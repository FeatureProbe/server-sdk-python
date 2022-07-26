# -*- coding: UTF-8 -*-

# Copyright 2022 FeatureProbe
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import contextlib
import json
import logging
import queue
import threading
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
from enum import Enum
from queue import Queue
from typing import List, Optional

import requests
from apscheduler.schedulers.background import BackgroundScheduler

from featureprobe.access_recorder import AccessRecorder
from featureprobe.context import Context
from featureprobe.event import Event, AccessEvent
from featureprobe.event_processor import EventProcessor


class _EventAction:
    class Type(Enum):
        EVENT = 1
        FLUSH = 2
        SHUTDOWN = 3

    def __init__(self, _type: Type, event: Optional[Event]):
        self.type = _type
        self.event = event


class _EventRepository:
    def __init__(self):
        self.events = []
        self.access = AccessRecorder()

    @classmethod
    def _clone(cls, events: List[Event], access: AccessRecorder) -> "_EventRepository":
        repo = cls()
        repo.events = events.copy()
        repo.access = access.snapshot()
        return repo

    def to_dict(self) -> dict:
        return {
            'events': self.events,
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
        return _EventRepository._clone(self.events, self.access)

    def clear(self):
        self.events.clear()
        self.access.clear()


class DefaultEventProcessor(EventProcessor):
    __logger = logging.getLogger('FeatureProbe-Event')
    __EVENT_BATCH_HANDLE_SIZE = 50
    __CAPACITY = 10000

    __LOG_BUSY_EVENT = 'Event processing is busy, some will be dropped'

    def __init__(self, context: Context):
        self._closed = False
        self._events = Queue(maxsize=DefaultEventProcessor.__CAPACITY)

        self._api_url = context.event_url
        self._session = requests.Session()
        self._session.mount('http://', context.http_config.adapter)
        self._session.mount('https://', context.http_config.adapter)
        self._session.headers = {'Authorization', context.sdk_key}
        self._timeout = (context.http_config.conn_timeout, context.http_config.read_timeout)

        event_repository = _EventRepository()
        handler_thread = threading.Thread(target=self._handle_event,
                                          args=(self._events, event_repository),
                                          daemon=True)
        handler_thread.start()

        self._executor = ThreadPoolExecutor(max_workers=5)
        self._scheduler = BackgroundScheduler()
        self._scheduler.start()
        self._scheduler.add_job(self.flush,
                                trigger='interval',
                                seconds=5,
                                next_run_time=datetime.now())

    @classmethod
    def from_context(cls, context: Context) -> EventProcessor:
        return cls(context)

    def push(self, event: Event):
        if not self._closed:
            try:
                self._events.put_nowait(_EventAction(_EventAction.Type.EVENT, event))
            except queue.Full:
                DefaultEventProcessor.__logger.warning(DefaultEventProcessor.__LOG_BUSY_EVENT)

    def flush(self):
        if not self._closed:
            try:
                self._events.put_nowait(_EventAction(_EventAction.Type.FLUSH, None))
            except queue.Full:
                DefaultEventProcessor.__logger.warning(DefaultEventProcessor.__LOG_BUSY_EVENT)

    def shutdown(self):
        if self._closed:
            return
        self._closed = True
        self._events.put(_EventAction(_EventAction.Type.FLUSH, None))
        self._events.put(_EventAction(_EventAction.Type.SHUTDOWN, None))

    def _handle_event(self, events: Queue, event_repo: _EventRepository):
        actions = []
        while not self._closed or not events.empty():
            actions.clear()
            actions.append(events.get())
            with contextlib.suppress(queue.Empty):
                actions.extend(events.get_nowait()
                               for _ in range(1, DefaultEventProcessor.__EVENT_BATCH_HANDLE_SIZE))
            try:
                for action in actions:
                    if action.type == _EventAction.Type.EVENT:
                        self.__process_event(action.event, event_repo)
                    elif action.type == _EventAction.Type.FLUSH:
                        self.__process_flush(event_repo)
                    elif action.type == _EventAction.Type.SHUTDOWN:
                        self.__do_shutdown()
            except Exception as e:
                self.__logger.error('FeatureProbe event handle error', exc_info=e)

    def __do_shutdown(self):
        self._executor.shutdown(wait=False)

    def __process_event(self, event: Event, event_repo: _EventRepository):
        event_repo.add(event)

    def _send_events(self, repositories: List[_EventRepository]):
        repositories = [repo.to_dict() for repo in repositories]
        resp = self._session.post(self._api_url, json=json.dumps(repositories), timeout=self._timeout)
        self.__logger.debug('Http response: %s' % resp.text)  # sourcery skip: replace-interpolation-with-fstring
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            self.__logger.error('Unexpected error from event sender', exc_info=e)

    def __process_flush(self, event_repo: _EventRepository):
        if not event_repo:
            return
        send_queue = [event_repo.snapshot()]
        self._executor.submit(self._send_events, send_queue)
        event_repo.clear()
