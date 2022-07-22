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


import logging
import time
from typing import List, Dict, Union

from featureprobe.model.predicate import ConditionType, Predicate
from featureprobe.model.segment import Segment
from featureprobe.user import User


class Condition:
    __logger = logging.getLogger('FeatureProbe-Evaluator')

    def __init__(self,
                 cond_type: ConditionType = None,
                 subject: str = '',
                 predicate: Predicate = None,
                 objects: List[str] = None):
        self._type = cond_type
        self._subject = subject
        self._predicate = predicate
        self._objects = objects or []

    def match_objects(self, usr: User, segments: Dict[str, Segment]) -> bool:
        if self._type is None or self._predicate is None:
            return False

        matcher_proc = {
            ConditionType.STRING: self._match_string_condition,
            ConditionType.SEGMENT: self._match_segment_condition,
            ConditionType.DATETIME: self._match_datetime_condition,
            ConditionType.NUMBER: self._match_number_condition,
            ConditionType.SEMVER: self._match_semver_condition,
        }

        match = matcher_proc.get(self._type, default=Condition._match_dummy_condition)
        return match({
            'usr': usr,
            'segments': segments,
        })

    def _match_string_condition(self, usr: User, **_) -> bool:
        subject_val = usr[self._subject]
        if not subject_val:
            return False
        return self._predicate.matcher(subject_val, self._objects)

    def _match_segment_condition(self, user: User, segments: Dict[str, Segment], **_) -> bool:
        return self._predicate.matcher(user, segments, self._objects)

    def _match_datetime_condition(self, usr: User, **_):  # sourcery skip: replace-interpolation-with-fstring
        cv = usr[self._subject] or time.time()
        try:
            cv = int(cv)
        except ValueError:
            self.__logger.error('User attribute type mismatch. attribute value: %s, target type int' % cv)
            return False

        try:
            return self._predicate.matcher(cv, self._objects)
        except ValueError as e:
            self.__logger.error('Met a string that cannot be parsed to int in Condition.objects: %s' % str(e))
            return False

    def _match_number_condition(self, usr: User, **_):  # sourcery skip: replace-interpolation-with-fstring
        cv = usr[self._subject]
        if not cv:
            return False
        try:
            cv = float(cv)
        except ValueError:
            self.__logger.error('User attribute type mismatch. attribute value: %s, target type float' % cv)
            return False

        try:
            return self._predicate.matcher(cv, self._objects)
        except ValueError as e:
            self.__logger.error('Met a string that cannot be parsed to float in Condition.objects: %s' % str(e))
            return False

    def _match_semver_condition(self, usr: User, **_):
        # TODO
        raise NotImplementedError()

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
    def predicate(self, value: Predicate):
        self._predicate = value

    @property
    def objects(self) -> List[str]:
        return self._objects

    @objects.setter
    def objects(self, value: List[str]):
        self._objects = value
