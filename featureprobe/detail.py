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

from typing import Dict, Optional


class Detail:
    def __init__(self, value=None, reason: Optional[str] = None,
                 rule_index: Optional[int] = None, version: Optional[int] = None):
        self._value = value
        self._rule_index = rule_index
        self._version = version
        self._reason = reason

    def __str__(self):
        return 'FPDetail{value=%s, rule_index=%s, version=%s, reason=\'%s\'}' % \
               (self._value, self._rule_index, self._version, self._reason)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def rule_index(self):
        return self._rule_index

    @rule_index.setter
    def rule_index(self, rule_index):
        self._rule_index = rule_index

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        self._version = version

    @property
    def reason(self):
        return self._reason

    @reason.setter
    def reason(self, reason):
        self._reason = reason
