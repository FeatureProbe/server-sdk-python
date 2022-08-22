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

import re
from enum import Enum

from featureprobe.internal.semver import SemVer


class Predicate(str, Enum):
    def __new__(cls, value, matcher=None):
        if isinstance(value, cls):
            return value
        if matcher is None:
            return cls._value2member_map_[value]

        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.matcher = matcher
        return obj

    def __str__(self):
        return self.value


class StringPredicate(Predicate):
    IS_ONE_OF = 'is one of', lambda target, objects: \
        target in objects

    ENDS_WITH = 'ends with', lambda target, objects: \
        any(target.endswith(o) for o in objects)

    STARTS_WITH = 'starts with', lambda target, objects: \
        any(target.startswith(o) for o in objects)

    CONTAINS = 'contains', lambda target, objects: \
        any(o in target for o in objects)

    MATCHES_REGEX = 'matches regex', lambda target, objects: \
        any(re.search(pattern=o, string=target) for o in objects)

    IS_NOT_ANY_OF = 'is not any of', lambda target, objects: \
        target not in objects

    DOES_NOT_END_WITH = 'does not end with', lambda target, objects: \
        all(not target.endswith(o) for o in objects)

    DOES_NOT_START_WITH = 'does not start with', lambda target, objects: \
        all(not target.startswith(o) for o in objects)

    DOES_NOT_CONTAIN = 'does not contain', lambda target, objects: \
        all(o not in target for o in objects)

    DOES_NOT_MATCH_REGEX = 'does not match regex', lambda target, objects: \
        all(not re.search(pattern=o, string=target) for o in objects)


class SegmentPredicate(Predicate):
    IS_IN = 'is in', lambda user, segments, objects: \
        any(segments.get(s).contains(user, segments) for s in objects)

    IS_NOT_IN = 'is not in', lambda user, segments, objects: \
        all(not segments.get(s).contains(user, segments) for s in objects)


class DatetimePredicate(Predicate):
    AFTER = 'after', lambda target, objects: \
        any(target >= int(o) for o in objects)

    BEFORE = 'before', lambda target, objects: \
        any(target < int(o) for o in objects)


class NumberPredicate(Predicate):
    EQUAL = '=', lambda custom_value, objects: \
        any(custom_value == float(o) for o in objects)

    NOT_EQUAL = '!=', lambda custom_value, objects: \
        all(custom_value != float(o) for o in objects)

    GREATER_THAN = '>', lambda custom_value, objects: \
        any(custom_value > float(o) for o in objects)

    GREATER_OR_EQUAL = '>=', lambda custom_value, objects: \
        any(custom_value >= float(o) for o in objects)

    LESS_THAN = '<', lambda custom_value, objects: \
        any(custom_value < float(o) for o in objects)

    LESS_OR_EQUAL = '<=', lambda custom_value, objects: \
        any(custom_value <= float(o) for o in objects)


class SemverPredicate(Predicate):
    EQUAL = '=', lambda custom_value, objects: \
        any(custom_value == SemVer(o) for o in objects)

    NOT_EQUAL = '!=', lambda custom_value, objects: \
        all(custom_value != SemVer(o) for o in objects)

    GREATER_THAN = '>', lambda custom_value, objects: \
        any(custom_value > SemVer(o) for o in objects)

    GREATER_OR_EQUAL = '>=', lambda custom_value, objects: \
        any(custom_value >= SemVer(o) for o in objects)

    LESS_THAN = '<', lambda custom_value, objects: \
        any(custom_value < SemVer(o) for o in objects)

    LESS_OR_EQUAL = '<=', lambda custom_value, objects: \
        any(custom_value <= SemVer(o) for o in objects)


class ConditionType(str, Enum):
    def __new__(cls, value, predicates):
        if isinstance(value, cls):
            return value
        if predicates is None:
            return cls._value2member_map_[value]

        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.predicates = predicates
        return obj

    def __str__(self):
        return self.value

    STRING = 'string', StringPredicate
    SEGMENT = 'segment', SegmentPredicate
    DATETIME = 'datetime', DatetimePredicate
    NUMBER = 'number', NumberPredicate
    SEMVER = 'semver', SemverPredicate
