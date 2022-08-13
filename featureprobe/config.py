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

from datetime import timedelta
from enum import Enum
from typing import Union

from featureprobe.default_event_processor import DefaultEventProcessor
from featureprobe.file_synchronizer import FileSynchronizer
from featureprobe.http_config import HttpConfig
from featureprobe.internal.defaultable import defaultable
from featureprobe.memory_data_repository import MemoryDataRepository
from featureprobe.pooling_synchronizer import PoolingSynchronizer


class SyncMode(str, Enum):
    def __new__(cls, value, synchronizer_creator):
        if isinstance(value, cls):
            return value
        if synchronizer_creator is None:
            return cls._value2member_map_[value]

        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.synchronizer_creator = synchronizer_creator
        return obj

    POOLING = 'pooling', PoolingSynchronizer.from_context
    FILE = 'file', FileSynchronizer.from_context


@defaultable
class Config:

    def __init__(self,
                 location: str = None,
                 sync_mode: Union[str, SyncMode] = SyncMode.POOLING,
                 synchronizer_url: str = None,
                 event_url: str = None,
                 remote_uri: str = 'http://127.0.0.1:4007',
                 http_config: HttpConfig = HttpConfig(),
                 refresh_interval: Union[timedelta, float] = timedelta(seconds=5),
                 ):
        self._location = location
        self._synchronizer_creator = SyncMode(sync_mode).synchronizer_creator
        self._data_repository_creator = MemoryDataRepository.from_context
        self._event_processor_creator = DefaultEventProcessor.from_context
        self._synchronizer_url = synchronizer_url
        self._event_url = event_url
        self._remote_uri = remote_uri
        self._http_config = http_config or HttpConfig()
        self._refresh_interval = refresh_interval \
            if isinstance(refresh_interval, timedelta) \
            else timedelta(seconds=refresh_interval)

    @property
    def location(self):
        return self._location

    @property
    def synchronizer_creator(self):
        return self._synchronizer_creator

    @property
    def data_repository_creator(self):
        return self._data_repository_creator

    @property
    def event_processor_creator(self):
        return self._event_processor_creator

    @property
    def synchronizer_url(self):
        return self._synchronizer_url

    @property
    def event_url(self):
        return self._event_url

    @property
    def remote_uri(self):
        return self._remote_uri

    @property
    def http_config(self):
        return self._http_config

    @property
    def refresh_interval(self):
        return self._refresh_interval
