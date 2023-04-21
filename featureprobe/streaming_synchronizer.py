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
import threading
from platform import python_version
from urllib.parse import urlparse

from featureprobe.realtime import RealtimeToggleUpdateNS

from sys import version_info as python_version

if python_version >= (3, 6):
    import socketio

from featureprobe.polling_synchronizer import PollingSynchronizer
from featureprobe.synchronizer import Synchronizer


class StreamingSynchronizer(Synchronizer):
    __logger = logging.getLogger('FeatureProbe-Synchronizer')

    def __init__(
            self,
            context: "Context",
            data_repo: "DataRepository",
            ready: "threading.Event"):
        self.__polling_synchronizer = PollingSynchronizer.from_context(
            context, data_repo, ready)
        self._realtime_url = context.realtime_url
        self._socket = None
        self._context = context
        self._lock = threading.RLock()

    @classmethod
    def from_context(
            cls,
            context: "Context",
            data_repo: "DataRepository",
            ready: "Event") -> "Synchronizer":
        return cls(context, data_repo, ready)

    def start(self):
        self._connect_socket(self._context)
        self.__polling_synchronizer.start()

    def sync(self):
        self.__polling_synchronizer.sync()

    def close(self):
        self.__polling_synchronizer.close()
        with self._lock:
            if self._socket is not None:
                with contextlib.suppress(Exception):
                    self._socket.disconnect()
                    self._socket = None

    def initialized(self):
        return self.__polling_synchronizer.initialized()

    def _connect_socket(self, context: "Context"):
        if self._socket is not None:
            return

        if python_version < (3, 6):
            self.__logger.info(
                'python version %s does not support socketio, realtime toggle updating is disabled'
                % ('.'.join(map(str, python_version))))
            return

        path = urlparse(context.realtime_url).path
        self._socket = socketio.Client()
        self._socket.register_namespace(
            RealtimeToggleUpdateNS(
                path, context, self))

        try:
            self.__logger.info(
                "connecting socket to {}, path={}".format(
                    context.realtime_url, path))
            self._socket.connect(
                context.realtime_url,
                transports=["websocket"],
                socketio_path=path,
                wait=False,
                wait_timeout=10,
            )
        except socketio.exceptions.ConnectionError as e:
            self.__logger.error(
                "failed to connect socket, realtime toggle updating is disabled",
                exc_info=e,
            )
            self._socket = None
