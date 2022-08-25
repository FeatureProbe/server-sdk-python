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

from typing import Dict
import uuid


class User:
    def __init__(self, stable_rollout_key: str = None,
                 attrs: Dict[str, str] = None):
        self._key = stable_rollout_key or str(uuid.uuid1())
        self._attrs = attrs or {}

    def __setitem__(self, key: str, value: str):
        self._attrs[key] = value

    def __getitem__(self, item: str):
        try:
            return self._attrs[item]
        except KeyError:
            return None

    def __delitem__(self, key: str):
        self._attrs.pop(key, None)

    def stable_rollout(self, key):
        self._key = key
        return self

    def to_dict(self) -> dict:
        return {
            'key': self._key,
            'attrs': self._attrs,
        }

    @property
    def key(self) -> str:
        return self._key

    @property
    def attrs(self) -> Dict[str, str]:
        return self._attrs

    @attrs.setter
    def attrs(self, attrs: Dict[str, str]):
        self._attrs = attrs

    def with_attr(self, key: str, value: str):
        self._attrs[key] = value

    def has_attr(self, attr: str):
        return attr in self._attrs
