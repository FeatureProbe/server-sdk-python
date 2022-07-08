import logging
import sched
import threading

import aiohttp

from data_repository import DataRepository
from fp_context import FPContext
from synchronizer import Synchronizer


class PoolingSynchronizer(Synchronizer):
    __logger = logging.getLogger('FeatureProbe-Synchronizer')
    __GET_SDK_KEY_HEADER = 'Authorization'
    __lock = threading.RLock()

    def __init__(self, context: FPContext, data_repo: DataRepository):
        self._refresh_interval = context.refresh_interval
        self._api_url = context.synchronizer_url
        self._data_repository = data_repo
        self.headers = {PoolingSynchronizer.__GET_SDK_KEY_HEADER, context.server_sdk_key}
        self.http_client = aiohttp.ClientSession(
            connector=context.http_configuration.connecter,
            conn_timeout=context.http_configuration.conn_timeout,
            read_timeout=context.http_configuration.read_timeout
        )
        self._scheduler = sched.scheduler()

    def sync(self):
        PoolingSynchronizer.__logger.info(
            'Starting FeatureProbe polling repository with interval %d ms' % self._refresh_interval)  # FIXME: use datetime.timedelta as Duration, get ms
        self.__poll()
        with PoolingSynchronizer.__lock:
            if self._worker is None:
                self._worker = self._

    def close(self):
        PoolingSynchronizer.__logger.info('Closing FeatureProbe PollingSynchronizer')
        with PoolingSynchronizer.__lock:
            self._scheduler.empty()

    async def __poll(self):  # async
        async with self.http_client.get(self._api_url, headers=self.headers) as req:
            resp = await req.json()
            