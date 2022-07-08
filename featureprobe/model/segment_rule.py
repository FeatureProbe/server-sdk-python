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

from typing import List, Dict
from model.condition import Condition
from model.segment import Segment
from featureprobe.fp_user import FPUser
from featureprobe.hit_result import HitResult

class SegmentRule:
    def __init__(self, conditions: List[Condition] = None):
        self._conditions = conditions or []

    @property
    def conditions(self) -> List[Condition]:
        return self._conditions

    @conditions.setter
    def conditions(self, cond: List[Condition]):
        self._conditions = cond

    def hit(self, user: FPUser, segments: Dict[str, Segment]) -> HitResult:
        for condition in self._conditions:
            if condition.type != condition.ConditionType.SEGMENT and not user.has_attr(condition.subject):
                return HitResult(False,
                                 reason='Warning: User with key \'%s\' does not have attribute name \'%s\''
                                        % (user.key, condition.subject))
            if not condition.match_objects(user, segments):
                return HitResult(False)

        return HitResult(True)
