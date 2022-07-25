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


import asyncio
import contextlib
import logging
from apscheduler.schedulers.background import BackgroundScheduler
import threading
from asyncio import Queue, QueueFull, QueueEmpty
from enum import Enum
from typing import List, Optional

import aiohttp

from access_recorder import AccessRecorder
from event import Event, AccessEvent
from event_processor import EventProcessor
from featureprobe.context import Context


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


class _SendEventsTask(threading.Thread):
    GET_SDK_KEY_HEADER = 'Authorization'

    def __init__(self, context: Context, repositories: List[_EventRepository]):
        self.repositories = repositories
        self.api_url = context.event_url
        self.headers = {_SendEventsTask.GET_SDK_KEY_HEADER, context.sdk_key}
        self.http_client = aiohttp.ClientSession(
            connector=context.http_config.connecter,
            conn_timeout=context.http_config.conn_timeout,
            read_timeout=context.http_config.read_timeout
        )

    def run(self) -> None:
        # FIXME
        pass

    """
        Request request;
        try {
            RequestBody requestBody = RequestBody.create(MediaType.parse("application/json"),
                    mapper.writeValueAsString(repositories));
            request = new Request.Builder()
                    .url(apiUrl.toString())
                    .headers(headers)
                    .post(requestBody)
                    .build();
        } catch (Exception e) {
            logger.error(LOG_SENDER_ERROR, e);
            return;
        }
        try (Response response = httpClient.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new HttpErrorException("Http request error: " + response.code());
            }
            logger.debug("Http response: {}", response);
        } catch (Exception e) {
            logger.error(LOG_SENDER_ERROR, e);
        }
    """


class DefaultEventProcessor(EventProcessor):
    __logger = logging.getLogger('FeatureProbe-Event')
    __EVENT_BATCH_HANDLE_SIZE = 50
    __CAPACITY = 10000

    __LOG_SENDER_ERROR = 'Unexpected error from event sender'
    __LOG_BUSY_EVENT = 'Event processing is busy, some will be dropped'

    def __init__(self, context: Context):
        self._closed = False
        self._events = Queue(DefaultEventProcessor.__CAPACITY)
        # self._executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix='FeatureProbe_event_handle')
        # FIXME
        event_repository = _EventRepository()
        threading.Thread(target=self.__handle_event(context, self._events, event_repository),
                         name='FeatureProbe_event_dispatch',
                         daemon=True).start()

        self._scheduler = sched.scheduler()
        threading.Thread(target=self.__schedule_flush, name='FeatureProbe_scheduled_flush', daemon=True).start()

    @classmethod
    def from_context(cls, context: Context) -> EventProcessor:
        return cls(context)

    async def push(self, event: Event):
        if not self._closed:
            await self._events.put(_EventAction(_EventAction.Type.EVENT, event))

    def push_nowait(self, event: Event):
        if not self._closed:
            try:
                self._events.put_nowait(_EventAction(_EventAction.Type.EVENT, event))
            except QueueFull:
                DefaultEventProcessor.__logger.warning(DefaultEventProcessor.__LOG_BUSY_EVENT)

    def __scheduled_flush(self):
        self._scheduler.enter(delay=5, priority=1, action=self.__scheduled_flush)
        self.flush_nowait()

    def scheduled(self, delay, func):
        def wrapper(*args, **kwargs):
            self._scheduler.enter(delay=delay, priority=1, action=func)




    def __schedule_flush(self):
        self._scheduler.enter(delay=0, priority=1, action=self.__scheduled_flush)
        self._scheduler.run()

    async def flush(self):
        if not self._closed:
            await self._events.put(_EventAction(_EventAction.Type.FLUSH, None))

    def flush_nowait(self):
        if not self._closed:
            try:
                self._events.put_nowait(_EventAction(_EventAction.Type.FLUSH, None))
            except QueueFull:
                DefaultEventProcessor.__logger.warning(DefaultEventProcessor.__LOG_BUSY_EVENT)

    async def shutdown(self):
        if self._closed:
            return
        self._closed = True
        await self._events.put(_EventAction(_EventAction.Type.FLUSH, None))
        await self._events.put(_EventAction(_EventAction.Type.SHUTDOWN, None))

    def __handle_event(self, context: Context, events: Queue, event_repo: _EventRepository):
        actions = []
        while not self._closed or events:
            # actions.append(asyncio.run(events.get()))
            aaa = asyncio.get_event_loop().run_until_complete(events.get())
            actions.append(aaa)
            with contextlib.suppress(QueueEmpty):
                actions.extend(events.get_nowait()
                               for _ in range(1, DefaultEventProcessor.__EVENT_BATCH_HANDLE_SIZE))
            try:
                for action in actions:
                    if action.type == _EventAction.Type.EVENT:
                        self.__process_event(action.event, event_repo)
                    elif action.type == _EventAction.Type.FLUSH:
                        self.__process_flush(context, event_repo)
                    elif action.type == _EventAction.Type.SHUTDOWN:
                        self.__do_shutdown()
            except Exception as e:
                self.__logger.error('FeatureProbe event handle error', exc_info=e)  # FIXME

    # async def __handle_event(self, context: FPContext, events: Queue, event_repo: EventRepository):
    #     actions = []
    #     while not self._closed or events:
    #         actions.append(await events.get())
    #         with contextlib.suppress(QueueEmpty):
    #             actions.extend(events.get_nowait()
    #                            for _ in range(1, DefaultEventProcessor.__EVENT_BATCH_HANDLE_SIZE))
    #         try:
    #             for action in actions:
    #                 if action.type == EventAction.Type.EVENT:
    #                     self.__process_event(action.event, event_repo)
    #                 elif action.type == EventAction.Type.FLUSH:
    #                     self.__process_flush(context, event_repo)
    #                 elif action.type == EventAction.Type.SHUTDOWN:
    #                     self.__do_shutdown()
    #         except Exception as e:
    #             self.__logger.error('FeatureProbe event handle error', exc_info=e)  # FIXME
    #
    def __do_shutdown(self):
        self._executor.shutdown(wait=False)

    def __process_event(self, event: Event, event_repo: _EventRepository):
        event_repo.add(event)

    def __process_flush(self, context: Context, event_repo: _EventRepository):
        if not event_repo:  # FIXME  eventRepository.isEmpty()
            return

        send_queue = [event_repo.snapshot()]
        send_task = _SendEventsTask(context, send_queue)

        # FIXME:::::::: run send_task, say POST the send_queue
        self._executor.submit(send_task.run)
        # executor.submit(task);   in java

        event_repo.clear()
