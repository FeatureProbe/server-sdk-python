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
from enum import Enum
from typing import Dict, Optional

from default_event_processor_factory import DefaultEventProcessorFactory
from file_synchronizer_facrory import FileSynchronizerFactory
from http_configuration import HttpConfiguration
from internal.wrapper_default import defaultable
from memory_data_repository_factory import MemoryDataRepositoryFactory
from pooling_synchronizer_factory import PoolingSynchronizerFactory


class SyncMode(Enum, str):
    POOLING = 'pooling'
    FILE = 'file'


@defaultable
class FPConfig:

    def __init__(self,
                 location: str,
                 sync_mode: SyncMode,
                 http_configuration: Optional[HttpConfiguration] = None,
                 remote_uri='http://127.0.0.1:4007',
                 synchronizer_url: str = None,
                 event_url: str = None,
                 refresh_interval: int = 5,  # sec
                 ):
        self._data_repository_factory = MemoryDataRepositoryFactory()
        self._remote_uri = remote_uri or 'http://127.0.0.1:4007'
        self._synchronizer_url = synchronizer_url
        self._event_url = event_url
        self._refresh_interval = refresh_interval
        self._location = location
        self._synchronizer_factory = FileSynchronizerFactory() if sync_mode is SyncMode.FILE \
            else PoolingSynchronizerFactory()
        self._http_configuration = http_configuration or HttpConfiguration()
        self._event_processor_factory = DefaultEventProcessorFactory()

    @property
    def data_repository_factory(self):
        return self._data_repository_factory

    @property
    def refresh_interval(self):
        return self._refresh_interval

    @property
    def location(self):
        return self._location

    @property
    def synchronizer_factory(self):
        return self._synchronizer_factory

    @property
    def synchronizer_url(self):
        return self._synchronizer_url

    @property
    def remote_uri(self):
        return self._remote_uri

    @property
    def event_url(self):
        return self._event_url

    @property
    def http_configuration(self):
        return self._http_configuration

    @property
    def event_processor_factory(self):
        return self._event_processor_factory
