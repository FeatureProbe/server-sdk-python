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

import logging
import time
from typing import List, Dict, Union, Optional, TYPE_CHECKING

from featureprobe.internal.empty_str import empty_str
from featureprobe.internal.json_decoder import json_decoder
from featureprobe.internal.semver import SemVer
from featureprobe.internal.stringifiable import stringifiable
from featureprobe.model.predicate import ConditionType, Predicate

if TYPE_CHECKING:
    from featureprobe.model.segment import Segment
    from featureprobe.user import User


@stringifiable
class Condition:
    _logger = logging.getLogger('FeatureProbe-Evaluator')

    def __init__(self,
                 subject: str,
                 type_: Union["ConditionType", str],
                 predicate: Union["Predicate", str],
                 objects: List[str]):
        self._subject = subject
        try:
            self._type = ConditionType(type_)
        except ValueError:
            self._type = None
        if isinstance(predicate, Predicate):
            self._predicate = predicate
        elif self._type is not None:
            try:
                self._predicate = self._type.predicates(predicate)
            except ValueError:
                self._predicate = None
        else:
            self._predicate = None
        self._objects = objects or []

    @classmethod
    @json_decoder
    def from_json(cls, json: dict) -> "Condition":
        subject = json.get('subject')
        type_ = json.get('type')
        predicate = json.get('predicate')
        objects = json.get('objects')
        return cls(subject, type_, predicate, objects)

    def match_objects(self, user: "User",
                      segments: Optional[Dict[str, "Segment"]]) -> bool:
        if self._type is None or self._predicate is None:
            return False

        matcher_proc = {
            ConditionType.STRING: self._match_string_condition,
            ConditionType.SEGMENT: self._match_segment_condition,
            ConditionType.DATETIME: self._match_datetime_condition,
            ConditionType.NUMBER: self._match_number_condition,
            ConditionType.SEMVER: self._match_semver_condition,
        }

        match = matcher_proc.get(self._type, Condition._match_dummy_condition)
        return match(user=user, segments=segments)

    def _match_string_condition(self, user: "User", **_) -> bool:
        subject_val = user[self._subject]
        if empty_str(subject_val):
            return False
        return self._predicate.matcher(subject_val, self._objects)

    def _match_segment_condition(
            self, user: "User", segments: Dict[str, "Segment"], **_) -> bool:
        return self._predicate.matcher(user, segments or {}, self._objects)

    def _match_datetime_condition(self, user: "User", **_):
        cv = user[self._subject] or time.time()
        try:
            cv = int(cv)
        except ValueError:
            # sourcery skip: replace-interpolation-with-fstring
            self._logger.error(
                'User attribute type mismatch. attribute value: \'%s\', target type int' %
                cv)
            return False

        try:
            return self._predicate.matcher(cv, self._objects)
        except ValueError as e:
            self._logger.error(
                'Met a string that cannot be parsed to int in Condition.objects',
                exc_info=e)
            return False

    def _match_number_condition(self, user: "User", **_):
        cv = user[self._subject]
        if not cv:
            return False
        try:
            cv = float(cv)
        except ValueError:
            # sourcery skip: replace-interpolation-with-fstring
            self._logger.error(
                'User attribute type mismatch. attribute value: \'%s\', target type float' %
                cv)
            return False

        try:
            return self._predicate.matcher(cv, self._objects)
        except ValueError as e:
            self._logger.error(
                'Met a string that cannot be parsed to float in Condition.objects',
                exc_info=e)
            return False

    def _match_semver_condition(self, user: "User", **_):
        cv = user[self._subject]
        try:
            cv = SemVer(cv)
        except ValueError as e:
            # sourcery skip: replace-interpolation-with-fstring
            self._logger.error(
                'Invalid user attribute. attribute value: \'%s\', target type semver' %
                cv, exc_info=e)
            return False

        try:
            return self._predicate.matcher(cv, self._objects)
        except ValueError as e:
            self._logger.error(
                'Met a string that cannot be parsed to semver in Condition.objects',
                exc_info=e)
            return False

    @staticmethod
    def _match_dummy_condition(**_):
        return False

    @property
    def type(self) -> ConditionType:
        return self._type

    @type.setter
    def type(self, value: Union[ConditionType, str]):
        self._type = ConditionType(value)

    @property
    def subject(self) -> str:
        return self._subject

    @subject.setter
    def subject(self, value: str):
        self._subject = value

    @property
    def predicate(self) -> Predicate:
        return self._predicate

    @predicate.setter
    def predicate(self, value: Union[Predicate, str]):
        if isinstance(value, Predicate):
            self._predicate = value
        elif isinstance(value, str) and self._type is not None:
            self._predicate = self._type.predicates(value)

    @property
    def objects(self) -> List[str]:
        return self._objects

    @objects.setter
    def objects(self, value: List[str]):
        self._objects = value
