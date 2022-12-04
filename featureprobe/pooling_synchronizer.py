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
import time

import socketio
import threading
from datetime import datetime
from typing import TYPE_CHECKING
from urllib.parse import urlparse

import tzlocal
from apscheduler.schedulers.background import BackgroundScheduler
from requests import Session

from featureprobe.model import Repository
from featureprobe.realtime import RealtimeToggleUpdateNS
from featureprobe.synchronizer import Synchronizer

if TYPE_CHECKING:
    from featureprobe.context import Context
    from featureprobe.data_repository import DataRepository


class PoolingSynchronizer(Synchronizer):
    __logger = logging.getLogger('FeatureProbe-Synchronizer')

    def __init__(
            self,
            context: "Context",
            data_repo: "DataRepository",
            ready: "threading.Event"):
        self._refresh_interval = context.refresh_interval
        self._api_url = context.synchronizer_url
        self._data_repo = data_repo

        self._session = Session()
        self._session.mount('http://', context.http_config.adapter)
        self._session.mount('https://', context.http_config.adapter)
        self._session.headers.update(context.headers)
        self._timeout = (
            context.http_config.conn_timeout,
            context.http_config.read_timeout)

        self._socket: socketio.Client
        self._connect_socket(context)

        self._scheduler = None
        self._lock = threading.RLock()
        self._ready = ready

    @classmethod
    def from_context(
            cls,
            context: "Context",
            data_repo: "DataRepository",
            ready: "threading.Event") -> "Synchronizer":
        return cls(context, data_repo, ready)

    def start(self):
        PoolingSynchronizer.__logger.info(
            "Starting FeatureProbe polling repository with interval %d ms"
            % (self._refresh_interval.total_seconds() * 1000)
        )
        self.sync()
        with self._lock:
            self._scheduler = BackgroundScheduler(
                timezone=tzlocal.get_localzone(), logger=self.__logger
            )
            self._scheduler.start()
            self._scheduler.add_job(
                self.sync,
                trigger="interval",
                seconds=self._refresh_interval.total_seconds(),
                next_run_time=datetime.now(),
            )

    def close(self):
        PoolingSynchronizer.__logger.info(
            "Closing FeatureProbe PollingSynchronizer")
        with self._lock:
            self._scheduler.shutdown()
            self._scheduler = None
            self._ready.clear()
            if self._socket is not None:
                with contextlib.suppress(Exception):
                    self._socket.disconnect()

    def sync(self):
        try:
            resp = self._session.get(self._api_url, timeout=self._timeout)
            resp.raise_for_status()
            self.__logger.debug('Http response: %d' % resp.status_code)
            body = resp.json()
            # sourcery skip: replace-interpolation-with-fstring
            self.__logger.debug('Http response body: %s' % body)
            repo = Repository.from_json(body)
            self._data_repo.refresh(repo)

            if not self._ready.is_set():
                self._ready.set()
        except Exception as e:  # noqa
            self.__logger.error(
                'Unexpected error from polling processor',
                exc_info=e)

    def _connect_socket(self, context: "Context"):
        path = urlparse(context.realtime_url).path
        self._socket = socketio.Client()
        self._socket.register_namespace(RealtimeToggleUpdateNS(path, context, self))

        try:
            self.__logger.info("connecting socket to {}, path={}".format(context.realtime_url, path))
            self._socket.connect(
                context.realtime_url,
                transports=["websocket"],
                socketio_path=path,
                wait=True,
                wait_timeout=1,
            )
        except socketio.exceptions.ConnectionError as e:
            self.__logger.error(
                "failed to connect socket, realtime toggle updating is disabled",
                exc_info=e,
            )
            self._socket = None

    def initialized(self) -> bool:
        return self._ready.is_set()



import asyncio

async def conn():
    # socket = socketio.Client()
    # # socket.on('connect', lambda: print('conn'))
    # socket.connect('https://featureprobe.io/server/realtime')
    print(1)
    await asyncio.sleep(1)
    print(1)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(conn())
    # asyncio.get_event_loop().run_until_complete(conn())
    print('out')
    time.sleep(10)
