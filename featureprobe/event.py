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
from fp_user import FPUser


class Event:

    def __init__(self, created_time: int, user: FPUser):
        self._created_time = created_time
        self._user = user

    @property
    def created_time(self) -> int:
        return self._created_time

    @property
    def user(self) -> FPUser:
        return self._user


class AccessEvent(Event):

    def __init__(self, timestamp: int, user: FPUser, key: str, value: str, version: int, index: int):
        super().__init__(timestamp, user)
        self._key = key
        self._value = value
        self._version = version
        self._index = index

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @property
    def version(self):
        return self._version

    @property
    def index(self):
        return self._index
