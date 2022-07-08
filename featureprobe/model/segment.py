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

from typing import List

from featureprobe.fp_user import FPUser
import segment_rule


class Segment:
    def __init__(self):
        self._unique_id = ''
        self._version = 0
        self._rules = []  # List[SegmentRule]

    @property
    def unique_id(self):
        return self._unique_id

    @unique_id.setter
    def unique_id(self, uid: str):
        self._unique_id = uid

    @property
    def version(self) -> int:
        return self._version

    @version.setter
    def version(self, version: int):
        self._version = version

    @property
    def rules(self) -> List[segment_rule.SegmentRule]:
        return self._rules

    @rules.setter
    def rules(self, rules: List[segment_rule.SegmentRule]):
        self._rules = rules

    def contain(self, user: FPUser, segments):
        for rule in self._rules:
            hit_result = rule.hit(user, segments)
            if hit_result.hit:
                return True

        return False
