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
import logging
import threading
import traceback
from datetime import datetime
from typing import TYPE_CHECKING

import aiohttp
from apscheduler.schedulers.background import BackgroundScheduler

from featureprobe import Repository
from featureprobe.internal.http_error import HTTPError
from featureprobe.synchronizer import Synchronizer

if TYPE_CHECKING:
    from featureprobe.context import Context
    from featureprobe.data_repository import DataRepository


class PoolingSynchronizer(Synchronizer):
    __logger = logging.getLogger('FeatureProbe-Synchronizer')

    _GET_SDK_KEY_HEADER = 'Authorization'

    def __init__(self, context: "Context", data_repo: "DataRepository"):
        self._refresh_interval = context.refresh_interval
        self._api_url = context.synchronizer_url
        self._data_repo = data_repo
        self._headers = {PoolingSynchronizer._GET_SDK_KEY_HEADER, context.sdk_key}
        self._web_client = aiohttp.ClientSession(
            connector=context.http_config.connector,
            conn_timeout=context.http_config.conn_timeout,
            read_timeout=context.http_config.read_timeout
        )
        self._scheduler = None
        self._loop = asyncio.get_event_loop()
        self._lock = threading.RLock()

    @classmethod
    def from_context(cls, context: "Context", data_repo: "DataRepository") -> "Synchronizer":
        return cls(context, data_repo)

    def sync(self):
        PoolingSynchronizer.__logger.info(
            'Starting FeatureProbe polling repository with interval %d ms'
            % self._refresh_interval.total_seconds() * 1000)
        with self._lock:
            self._scheduler = BackgroundScheduler()
            self._scheduler.start()
            self._scheduler.add_job(self._poll,
                                    trigger='interval',
                                    seconds=self._refresh_interval.total_seconds(),
                                    next_run_time=datetime.now())

    def close(self):
        PoolingSynchronizer.__logger.info('Closing FeatureProbe PollingSynchronizer')
        with self._lock:
            self._scheduler.shutdown()
            del self._scheduler

    def _poll(self):
        self._loop.run_until_complete(self._poll0())

    async def _poll0(self):
        try:
            async with self._web_client.get(self._api_url, headers=self._headers) as resp:
                if not 200 <= resp.status < 300:  # not success
                    raise HTTPError(resp.status)
                self.__logger.debug('Http response: %s' % resp)  # sourcery skip: replace-interpolation-with-fstring
                body = await resp.json()
                self.__logger.debug('Http response body: %s' % body)
                repo = Repository.from_json(body)
                self._data_repo.refresh(repo)
        except Exception:  # noqa
            self.__logger.error('Unexpected error from polling processor')
            self.__logger.error(traceback.format_exc())
