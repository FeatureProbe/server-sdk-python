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
    from featureprobe.client import Client


class RealtimeToggleUpdateNS(ClientNamespace):
    __logger = logging.getLogger("FeatureProbe-Socket")

    def __init__(self, namespace, fp_client: "Client"):
        super(RealtimeToggleUpdateNS, self).__init__(namespace=namespace)
        self._fp_client = fp_client

    def on_connect(self):
        self.__logger.info("connect socketio success")
        self.emit(
            "register", {"key": self._fp_client._sdk_key}  # noqa: access protected member
        )

    def on_connect_error(self, error):
        self.__logger.error("socketio error: {}".format(error))

    def on_disconnect(self):
        self.__logger.info("disconnecting socketio")

    def on_update(self, data):
        self.__logger.info("socketio recv update event")
        self._fp_client._synchronizer.sync()  # noqa: access protected member
