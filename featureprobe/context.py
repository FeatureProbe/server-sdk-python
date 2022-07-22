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


import logging

from featureprobe.config import Config


class Context:
    __logger = logging.getLogger('FeatureProbe')

    GET_REPOSITORY_DATA_API = '/api/server-sdk/toggles'
    POST_EVENTS_DATA_API = '/api/events'

    def __init__(self, server_sdk_key: str, config: Config):
        self._synchronizer_url = config.synchronizer_url or config.remote_uri + Context.GET_REPOSITORY_DATA_API
        self._event_url = config.event_url or config.remote_uri + Context.POST_EVENTS_DATA_API
        self._server_sdk_key = server_sdk_key
        self._refresh_interval = config.refresh_interval
        self._location = config.location
        self._http_configuration = config.http_configuration

    @property
    def synchronizer_url(self):
        return self._synchronizer_url

    @property
    def event_url(self):
        return self._event_url

    @property
    def server_sdk_key(self):
        return self._server_sdk_key

    @property
    def refresh_interval(self):
        return self._refresh_interval

    @property
    def location(self):
        return self._location

    @property
    def http_configuration(self):
        return self._http_configuration
