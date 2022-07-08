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

from model.condition import Condition, ConditionType
from featureprobe.fp_user import FPUser
from serve import Serve
from hit_result import HitResult
from segment import Segment


class Rule:
    def __init__(self,
                 serve: Serve = None,
                 conditions: List[Condition] = None):
        self._serve = serve
        self._conditions = conditions or []

    @property
    def serve(self) -> Serve:
        return self._serve

    @serve.setter
    def serve(self, serve: Serve):
        self._serve = serve

    @property
    def conditions(self) -> List[Condition]:
        return self._conditions

    @conditions.setter
    def conditions(self, conditions: List[Condition]):
        self._conditions = conditions

    def hit(self, user: FPUser, segments: Dict[str, Segment], toggle_key: str) -> HitResult:
        for condition in self._conditions:
            if condition.type not in (ConditionType.SEGMENT, ConditionType.DATETIME) \
                    and not user.has_attr(condition.subject):
                return HitResult(False,
                                 reason='Warning: User with key \'%s\' does not have attribute name \'%s\''
                                        % (user.key, condition.subject))
            if not condition.match_objects(user, segments):
                return HitResult(False)

        return self._serve.eval_index(user, toggle_key)
