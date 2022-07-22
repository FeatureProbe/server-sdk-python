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

from featureprobe.hit_result import HitResult
from featureprobe.model.condition import Condition
from featureprobe.user import User


class SegmentRule:
    def __init__(self, conditions: List[Condition] = None):
        self._conditions = conditions or []

    @property
    def conditions(self) -> List[Condition]:
        return self._conditions

    @conditions.setter
    def conditions(self, value: List[Condition]):
        self._conditions = value or []

    def hit(self,
            user: User,
            segments  # Dict[str, Segment]
            ) -> HitResult:
        for condition in self._conditions:
            if condition.type != condition.ConditionType.SEGMENT and not user.has_attr(condition.subject):
                return HitResult(False,
                                 reason='Warning: User with key \'%s\' does not have attribute name \'%s\''
                                        % (user.key, condition.subject))
            if not condition.match_objects(user, segments):
                return HitResult(False)

        return HitResult(True)


class Segment:
    def __init__(self):
        self._unique_id = ''
        self._version = 0
        self._rules = []  # List[SegmentRule]

    @property
    def unique_id(self):
        return self._unique_id

    @unique_id.setter
    def unique_id(self, value: str):
        self._unique_id = value

    @property
    def version(self) -> int:
        return self._version

    @version.setter
    def version(self, value: int):
        self._version = value

    @property
    def rules(self) -> List[SegmentRule]:
        return self._rules

    @rules.setter
    def rules(self, value: List[SegmentRule]):
        self._rules = value or []

    def contain(self, user: User, segments):
        for rule in self._rules:
            hit_result = rule.hit(user, segments)
            if hit_result.hit:
                return True

        return False
