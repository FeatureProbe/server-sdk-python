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


from typing import Dict


class User:

    def __init__(self, key: str):
        self._key = key
        self._attrs = {}

    def __setitem__(self, key, value):
        self._attrs[key] = value

    def __getitem__(self, item):
        return self._attrs[item]

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
