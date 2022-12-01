# Copyright 2022 FeatureProbe
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import contextlib
import logging
import queue
import threading
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
from enum import Enum
from queue import Queue
from typing import List, Optional

import tzlocal
from apscheduler.schedulers.background import BackgroundScheduler
from requests import Session, HTTPError

from featureprobe.access_recorder import AccessRecorder
from featureprobe.context import Context
from featureprobe.event import Event, AccessEvent
from featureprobe.event_processor import EventProcessor


class EventAction:
    class Type(Enum):
        EVENT = 1
        FLUSH = 2
        SHUTDOWN = 3

    def __init__(self, _type: Type, event: Optional[Event]):
        self.type = _type
        self.event = event


class EventRepository:
    def __init__(self):
        self.events = []
        self.access = AccessRecorder()

    @classmethod
    def _clone(
            cls,
            events: List[Event],
            access: AccessRecorder) -> "EventRepository":
        repo = cls()
        repo.events = events.copy()
        repo.access = access.snapshot()
        return repo

    def to_dict(self) -> dict:
        return {
            'events': [e.to_dict() for e in self.events],
            'access': self.access.to_dict(),
        }

    def __bool__(self):
        return not self.is_empty()

    def is_empty(self):
        return len(self.events) == 0 and len(self.access.counters) == 0

    def add(self, event: Event):
        if isinstance(event, AccessEvent):
            self.access.add(event)

    def snapshot(self):
        return EventRepository._clone(self.events, self.access)

    def clear(self):
        self.events.clear()
        self.access.clear()


class DefaultEventProcessor(EventProcessor):
    _logger = logging.getLogger('FeatureProbe-Event')
    _EVENT_BATCH_HANDLE_SIZE = 50
    _CAPACITY = 10000

    _LOG_BUSY_EVENT = 'Event processing is busy, some will be dropped'

    def __init__(self, context: Context):
        self._closed = False
        self._events = Queue(maxsize=DefaultEventProcessor._CAPACITY)

        self._api_url = context.event_url
        self._session = Session()
        self._session.mount('http://', context.http_config.adapter)
        self._session.mount('https://', context.http_config.adapter)
        self._session.headers.update(context.headers)
        self._timeout = (
            context.http_config.conn_timeout,
            context.http_config.read_timeout)

        self._event_repository = EventRepository()
        self._handler_thread = threading.Thread(
            target=self._handle_event, args=(
                self._events, self._event_repository), daemon=True)
        self._handler_thread.start()

        self._executor = ThreadPoolExecutor(max_workers=5)
        self._scheduler = BackgroundScheduler(
            timezone=tzlocal.get_localzone(), logger=self._logger)
        self._scheduler.start()
        self._scheduler.add_job(self.flush,
                                trigger='interval',
                                seconds=5,
                                next_run_time=datetime.now())

    @classmethod
    def from_context(cls, context: Context) -> EventProcessor:
        return cls(context)

    def push(self, event: Event):
        if self._closed:
            return
        try:
            self._events.put_nowait(EventAction(
                EventAction.Type.EVENT, event))
        except queue.Full:
            DefaultEventProcessor._logger.warning(
                DefaultEventProcessor._LOG_BUSY_EVENT)

    def flush(self, block=False, timeout=None):
        if self._closed:
            return
        try:
            self._events.put(
                EventAction(EventAction.Type.FLUSH, None), block, timeout)
        except queue.Full:
            DefaultEventProcessor._logger.warning(
                DefaultEventProcessor._LOG_BUSY_EVENT)

    def shutdown(self):
        self._do_shutdown()

    def _handle_event(self, events: Queue, event_repo: EventRepository):
        actions = []
        while not self._closed or not events.empty():
            actions.clear()
            actions.append(events.get())
            with contextlib.suppress(queue.Empty):
                actions.extend(
                    events.get_nowait() for _ in range(
                        1, DefaultEventProcessor._EVENT_BATCH_HANDLE_SIZE))
            try:
                for action in actions:
                    if action.type == EventAction.Type.EVENT:
                        self._process_event(action.event, event_repo)
                    elif action.type == EventAction.Type.FLUSH:
                        self._process_flush(event_repo)
                    elif action.type == EventAction.Type.SHUTDOWN:
                        self._do_shutdown()
            except Exception as e:
                self._logger.error(
                    'FeatureProbe event handle error', exc_info=e)

    def _do_shutdown(self):
        if self._closed:
            return

        self.flush(block=True, timeout=2)
        self._closed = True
        self._handler_thread.join(2)
        self._scheduler.shutdown(wait=True)
        self._executor.shutdown(wait=True)

    def _process_event(self, event: Event, event_repo: EventRepository):
        event_repo.add(event)

    def _send_events(self, repositories: List[EventRepository]):
        repositories = [repo.to_dict() for repo in repositories]
        resp = self._session.post(
            self._api_url,
            json=repositories,
            timeout=self._timeout)
        # sourcery skip: replace-interpolation-with-fstring
        self._logger.debug('Http response: %s' % resp.text)
        try:
            resp.raise_for_status()
        except HTTPError as e:
            self._logger.error(
                'Unexpected error from event sender',
                exc_info=e)

    def _process_flush(self, event_repo: EventRepository):
        if not event_repo:
            return
        send_queue = [event_repo.snapshot()]
        self._executor.submit(self._send_events, send_queue)
        event_repo.clear()
