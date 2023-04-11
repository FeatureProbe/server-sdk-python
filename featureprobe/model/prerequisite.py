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
from featureprobe.internal.json_decoder import json_decoder


class Prerequisite:
    def __init__(self, key: str, value):
        self._key = key
        self._value = value

    @classmethod
    @json_decoder
    def from_json(cls, json: dict) -> "Prerequisite":
        key = json.get('key')
        value = json.get('value')
        return cls(key, value)

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value


class PrerequisiteError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)
