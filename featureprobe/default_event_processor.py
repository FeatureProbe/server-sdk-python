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
import logging
import threading
from asyncio import Queue, QueueFull, QueueEmpty
from enum import Enum
from typing import Union, List

import aiohttp

from event import Event, AccessEvent
from event_processor import EventProcessor
from concurrent.futures import ThreadPoolExecutor

from fp_context import FPContext
import sched


class EventAction:
    class Type(Enum):
        EVENT = 1
        FLUSH = 2
        SHUTDOWN = 3

    def __init__(self, _type: Type, event: Union[Event, None]):
        self.type = _type
        self.event = event


class EventRepository:
    def __init__(self, event_repository=None):
        if event_repository:
            self._events = event_repository.events
            self._access = event_repository.access.snapshot()
        else:
            self._events = []
            self._access = AccessRecoder()

    def __bool__(self):
        return self._events and self._access.counters.isEmpty()

    def add(self, event: Event):
        if isinstance(event, AccessEvent):
            self._access.add(event)

    def snapshot(self):
        return EventRepository(self)

    def clear(self):
        self._events.clear()
        self._access.clear()

    @property
    def events(self):
        return self._events

    @property
    def access(self):
        return self._access


class SendEventsTask(threading.Thread):
    __GET_SDK_KEY_HEADER = 'Authorization'

    def __init__(self, context: FPContext, repositories: List[EventRepository]):
        self.api_url = context.event_url
        self.headers = {SendEventsTask.__GET_SDK_KEY_HEADER, context.server_sdk_key}
        self.http_client = aiohttp.ClientSession(
            connector=context.http_configuration.connecter,
            conn_timeout=context.http_configuration.conn_timeout,
            read_timeout=context.http_configuration.read_timeout
        )

        self.repositories = repositories

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

    def __init__(self, context: FPContext):
        self._closed = False
        self._events = Queue(DefaultEventProcessor.__CAPACITY)
        self._executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix='FeatureProbe_event_handle')
        event_repository = EventRepository()
        threading.Thread(target=self.__handle_event(context, self._events, event_repository),
                         name='FeatureProbe_event_dispatch',
                         daemon=True).start()

        self._scheduler = sched.scheduler()
        threading.Thread(target=self.__schedule_flush, name='FeatureProbe_scheduled_flush', daemon=True).start()

    async def push(self, event: Event):
        if not self._closed:
            await self._events.put(EventAction(EventAction.Type.EVENT, event))

    def push_nowait(self, event: Event):
        if not self._closed:
            try:
                self._events.put_nowait(EventAction(EventAction.Type.EVENT, event))
            except QueueFull:
                DefaultEventProcessor.__logger.warning(DefaultEventProcessor.__LOG_BUSY_EVENT)

    def __scheduled_flush(self):
        self._scheduler.enter(delay=5, priority=1, action=self.__scheduled_flush)
        self.flush_nowait()

    def __schedule_flush(self):
        self._scheduler.enter(delay=0, priority=1, action=self.__scheduled_flush)
        self._scheduler.run()

    async def flush(self):
        if not self._closed:
            await self._events.put(EventAction(EventAction.Type.FLUSH, None))

    def flush_nowait(self):
        if not self._closed:
            try:
                self._events.put_nowait(EventAction(EventAction.Type.FLUSH, None))
            except QueueFull:
                DefaultEventProcessor.__logger.warning(DefaultEventProcessor.__LOG_BUSY_EVENT)

    async def shutdown(self):
        if self._closed:
            return
        self._closed = True
        await self._events.put(EventAction(EventAction.Type.FLUSH, None))
        await self._events.put(EventAction(EventAction.Type.SHUTDOWN, None))

    def __handle_event(self, context: FPContext, events: Queue, event_repo: EventRepository):
        actions = []
        while not self._closed or events:
            actions.append(events.get_nowait())
            with contextlib.suppress(QueueEmpty):
                actions.extend(events.get_nowait()
                               for _ in range(1, DefaultEventProcessor.__EVENT_BATCH_HANDLE_SIZE))
            try:
                for action in actions:
                    if action.type == EventAction.Type.EVENT:
                        self.__process_event(action.event, event_repo)
                    elif action.type == EventAction.Type.FLUSH:
                        self.__process_flush(context, event_repo)
                    elif action.type == EventAction.Type.SHUTDOWN:
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

    def __process_event(self, event: Event, event_repo: EventRepository):
        event_repo.add(event)

    def __process_flush(self, context: FPContext, event_repo: EventRepository):
        if not event_repo:  # FIXME  eventRepository.isEmpty()
            return

        send_queue = [event_repo.snapshot()]
        send_task = SendEventsTask(context, send_queue)

        # FIXME:::::::: run send_task, say POST the send_queue
        self._executor.submit(send_task.run)
        # executor.submit(task);   in java

        event_repo.clear()
