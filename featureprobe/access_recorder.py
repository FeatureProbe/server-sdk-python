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

from time import time
import copy

from featureprobe.event import AccessEvent


class AccessCounter:

    def __init__(self, value: str, version: int, index: int):
        self._VALUE = value
        self._VERSION = version
        self._INDEX = index
        self._count = 1

    @property
    def value(self):
        return self._VALUE

    @property
    def version(self):
        return self._VERSION

    @property
    def index(self):
        return self._INDEX

    def increment(self):
        self._count += 1

    def is_group(self, _event: AccessEvent):
        return self._VALUE == _event.value and self._VERSION == _event.version and self._INDEX == _event.index


class AccessRecorder:

    def __init__(self):
        self._counters = {}  # Dict[str, List[AccessCounter]]
        self._start_time = 0
        self._end_time = 0

    @property
    def counters(self):
        return self._counters

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    def add(self, _event: AccessEvent):
        if not self._counters:
            self._start_time = int(time() * 1000)
        counters = self._counters[_event.key]
        if counters:
            for counter in counters:
                if counter.is_group(_event):
                    counter.increment()
                    return
            counters.append(AccessCounter(_event.value, _event.version, _event.index))
        else:
            groups = [AccessCounter(_event.value, _event.version, _event.index)]
            self._counters[_event.key] = groups

    def snapshot(self):
        _snapshot = copy.deepcopy(self)
        _snapshot._end_time = int(time() * 1000)
        return _snapshot

    def clear(self):
        self._counters = {}
