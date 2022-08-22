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

from typing import List, TYPE_CHECKING, Dict

from featureprobe.hit_result import HitResult
from featureprobe.internal.json_decoder import json_decoder
from featureprobe.model.condition import Condition
from featureprobe.model.predicate import ConditionType

if TYPE_CHECKING:
    from featureprobe.user import User


class SegmentRule:
    def __init__(self, conditions: List["Condition"] = None):
        self._conditions = conditions or []

    @classmethod
    @json_decoder
    def from_json(cls, json: dict) -> "SegmentRule":
        conditions = [Condition.from_json(c)
                      for c in json.get('conditions', [])]
        return cls(conditions)

    @property
    def conditions(self) -> List["Condition"]:
        return self._conditions

    @conditions.setter
    def conditions(self, value: List["Condition"]):
        self._conditions = value or []

    def hit(self,
            user: "User",
            segments: Dict[str, "Segment"]
            ) -> HitResult:
        for condition in self._conditions:
            if condition.type != ConditionType.SEGMENT and not user.has_attr(
                    condition.subject):
                return HitResult(
                    hit=False, reason="Warning: User with key '%s' does not have attribute name '%s'" %
                    (user.key, condition.subject))
            if not condition.match_objects(user, segments):
                return HitResult(hit=False)

        return HitResult(True)


class Segment:
    def __init__(self,
                 uid: str,
                 version: int,
                 rules: List["SegmentRule"] = None):
        self._uid = uid
        self._version = version
        self._rules = rules or []

    @classmethod
    @json_decoder
    def from_json(cls, json: dict) -> "Segment":
        uid = json.get('uniqueId')
        version = json.get('version', 1)
        rules = [SegmentRule.from_json(r) for r in json.get('rules', [])]
        return cls(uid, version, rules)

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value: str):
        self._uid = value

    @property
    def version(self) -> int:
        return self._version

    @version.setter
    def version(self, value: int):
        self._version = value

    @property
    def rules(self) -> List["SegmentRule"]:
        return self._rules

    @rules.setter
    def rules(self, value: List["SegmentRule"]):
        self._rules = value or []

    def contains(self, user: "User", segments: Dict[str, "Segment"]):
        for rule in self._rules:
            hit_result = rule.hit(user, segments)
            if hit_result.hit:
                return True

        return False
