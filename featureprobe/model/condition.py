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
import re
from enum import Enum
from typing import List, Dict

from featureprobe.fp_user import FPUser
from model import segment


class ConditionType(str, Enum):
    STRING = 'string'
    SEGMENT = 'segment'
    DATETIME = 'datetime'
    NUMBER = 'number'
    SEMVER = 'semver'


class PredicateType(str, Enum):
    # string predicate
    IS_ONE_OF = 'is one of'
    ENDS_WITH = 'ends with'
    STARTS_WITH = 'starts with'
    CONTAINS = 'contains'
    MATCHES_REGEX = 'matches regex'
    IS_NOT_ANY_OF = 'is not any of'
    DOES_NOT_END_WITH = 'does not end with'
    DOES_NOT_START_WITH = 'does not start with'
    DOES_NOT_CONTAIN = 'does not contain'
    DOES_NOT_MATCH_REGEX = 'does not match regex'

    # segment predicate
    IS_IN = 'is in'
    IS_NOT_IN = 'is not in'

    # datetime predicate
    AFTER = 'after'
    BEFORE = 'before'

    # number predicate
    # semver predicate
    EQUAL = '='
    NOT_EQUAL = '!='
    GREATER_THAN = '>'
    GREATER_OR_EQUAL = '>='
    LESS_THAN = '<'
    LESS_OR_EQUAL = '<='


class Condition:
    __logger = logging.getLogger('FeatureProbe-Evaluator')

    __string_matchers = {
        PredicateType.IS_ONE_OF:
            lambda target, objects: target in objects,
        PredicateType.ENDS_WITH:
            lambda target, objects: any(o.endswith(target) for o in objects),
        PredicateType.STARTS_WITH:
            lambda target, objects: any(o.srartswith(target) for o in objects),
        PredicateType.CONTAINS:
            lambda target, objects: any(target in o for o in objects),
        PredicateType.MATCHES_REGEX:
            lambda target, objects: any(re.match(target, o) for o in objects),
        PredicateType.IS_NOT_ANY_OF:
            lambda target, objects: target not in objects,
        PredicateType.DOES_NOT_END_WITH:
            lambda target, objects: all(not o.endswith(target) for o in objects),
        PredicateType.DOES_NOT_START_WITH:
            lambda target, objects: all(not o.startswith(target) for o in objects),
        PredicateType.DOES_NOT_CONTAIN:
            lambda target, objects: all(target not in o for o in objects),
        PredicateType.DOES_NOT_MATCH_REGEX:
            lambda target, objects: all(not re.match(target, o) for o in objects),

        # TODO: more
    }

    __segment_matchers = {
        PredicateType.IS_IN:
            lambda user, segments, objects: any(segments.get(s).contains(user, segments) for s in objects),
        PredicateType.IS_NOT_IN:
            lambda user, segments, objects: all(not segments.get(s).contains(user, segments) for s in objects),
    }

    __datetime_matchers = {
        PredicateType.AFTER:
            lambda target, custom_value: custom_value >= target,
        PredicateType.BEFORE:
            lambda target, custom_value: custom_value < target,
    }

    __number_matchers = {
        PredicateType.EQUAL:
            lambda custom_value, objects: any(custom_value == float(o) for o in objects),
        PredicateType.NOT_EQUAL:
            lambda custom_value, objects: all(custom_value != float(o) for o in objects),
        PredicateType.GREATER_THAN:
            lambda custom_value, objects: any(custom_value > float(o) for o in objects),
        PredicateType.GREATER_OR_EQUAL:
            lambda custom_value, objects: any(custom_value >= float(o) for o in objects),
        PredicateType.LESS_THAN:
            lambda custom_value, objects: any(custom_value < float(o) for o in objects),
        PredicateType.LESS_OR_EQUAL:
            lambda custom_value, objects: any(custom_value <= float(o) for o in objects),
    }

    __semver_matchers = {

    }

    def __init__(self,
                 cond_type: ConditionType = None,
                 subject: str = '',
                 predicate: PredicateType = None,
                 objects: List[str] = None):
        self._type = cond_type
        self._subject = subject
        self._predicate = predicate
        self._objects = objects or []

    def match_objects(self, usr: FPUser, segments: Dict[str, segment.Segment]) -> bool:
        if self._type == ConditionType.STRING:
            return self.__match_string_condition(usr)
        elif self._type == ConditionType.SEGMENT:
            return self.__match_segment_condition(usr, segments)
        # elif self._type == ConditionType.DATE:
        #     return self.__match_date_condition(subject_val)
        else:
            return False

    def __match_string_condition(self, usr: FPUser) -> bool:
        subject_val = usr.attrs.get(self._subject)
        if not subject_val:
            return False

        matcher = self.__string_matchers.get(self._predicate)
        if matcher is None:
            return False
        return matcher(subject_val, self._objects)

    def __match_segment_condition(self, user: FPUser, segments: Dict[str, segment.Segment]) -> bool:
        matcher = self.__segment_matchers.get(self._predicate)
        if matcher is None:
            return False
        return matcher(user, segments, self._objects)

    @property
    def type(self) -> ConditionType:
        return self._type

    @type.setter
    def type(self, typ):
        self._type = ConditionType(typ)

    @property
    def subject(self) -> str:
        return self._subject

    @subject.setter
    def subject(self, subject: str):
        self._subject = subject

    @property
    def predicate(self) -> PredicateType:
        return self._predicate

    @predicate.setter
    def predicate(self, pred):
        self._predicate = PredicateType(pred)

    @property
    def objects(self) -> List[str]:
        return self._objects

    @objects.setter
    def objects(self, objs: List[str]):
        self._objects = objs
