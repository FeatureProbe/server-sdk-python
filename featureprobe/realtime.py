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

import logging
from socketio import ClientNamespace
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from featureprobe.context import Context
    from featureprobe.synchronizer import Synchronizer


class RealtimeToggleUpdateNS(ClientNamespace):
    __logger = logging.getLogger("FeatureProbe-Socket")

    def __init__(self, namespace, context: "Context", synchronizer: "Synchronizer"):
        super(RealtimeToggleUpdateNS, self).__init__(namespace=namespace)
        self._synchronizer = synchronizer
        self._sdk_key = context.sdk_key

    def on_connect(self):
        self.__logger.info("connect socketio success")
        print("connect socketio success")
        self.emit("register", {"key": self._sdk_key})

    def on_connect_error(self, error):
        self.__logger.error("socketio error: {}".format(error))

    def on_disconnect(self):
        self.__logger.info("disconnecting socketio")

    def on_update(self, data):
        self.__logger.info("socketio recv update event")
        print("socketio recv update event")
        self._synchronizer.sync()
