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

import time

import featureprobe as fp


def setup_function():
    global condition, user, segments  # noqa
    condition = fp.Condition(subject='userId',
                             type_='string',
                             predicate=None,
                             objects=None)
    user = fp.User(key='test_user')
    segments = {'test_project$test_segment': fp.Segment(
        uid='test_project$test_segment',
        version=1,
        rules=[fp.SegmentRule(conditions=[
            fp.Condition(
                subject='userId',
                type_='string',
                predicate=fp.StringPredicate.IS_ONE_OF,
                objects=['1', '2']
            )]
        )]
    )}


def test_string_is_one_of():
    condition.objects = ['12345', '987654', '665544', '13797347245']
    condition.predicate = fp.StringPredicate.IS_ONE_OF

    user['userId'] = '12345'
    assert condition.match_objects(user, segments)

    user['userId'] = '999999'
    assert not condition.match_objects(user, segments)

    user['userId'] = '\t \n  '
    assert not condition.match_objects(user, segments)


def test_string_ends_with():
    condition.objects = ['123', '888']
    condition.predicate = fp.StringPredicate.ENDS_WITH

    user['userId'] = '123123'
    assert condition.match_objects(user, segments)

    user['userId'] = '999999'
    assert not condition.match_objects(user, segments)

    del user['userId']
    assert not condition.match_objects(user, segments)


def test_string_starts_with():
    condition.objects = ['123']
    condition.predicate = fp.StringPredicate.STARTS_WITH

    user['userId'] = '123321'
    assert condition.match_objects(user, segments)

    user['userId'] = '3333'
    assert not condition.match_objects(user, segments)


def test_string_contains():
    condition.objects = ['123', '456']
    condition.predicate = fp.StringPredicate.CONTAINS

    user['userId'] = '456433'
    assert condition.match_objects(user, segments)

    user['userId'] = '999999'
    assert not condition.match_objects(user, segments)


def test_string_matches_regex():
    condition.objects = ['0?(13|14|15|18)[0-9]{9}']
    condition.predicate = fp.StringPredicate.MATCHES_REGEX

    user['userId'] = '13797347245'
    assert condition.match_objects(user, segments)

    user['userId'] = '122122'
    assert not condition.match_objects(user, segments)


def test_string_is_not_any_of():
    condition.objects = ['12345', '987654', '665544']
    condition.predicate = fp.StringPredicate.IS_NOT_ANY_OF

    user['userId'] = '999999999'
    assert condition.match_objects(user, segments)

    user['userId'] = '12345'
    assert not condition.match_objects(user, segments)


def test_string_does_not_end_with():
    condition.objects = ['123', '456']
    condition.predicate = fp.StringPredicate.DOES_NOT_END_WITH

    user['userId'] = '3333333'
    assert condition.match_objects(user, segments)

    user['userId'] = '456456'
    assert not condition.match_objects(user, segments)


def test_string_does_not_start_with():
    condition.objects = ['123', '456']
    condition.predicate = fp.StringPredicate.DOES_NOT_START_WITH

    user['userId'] = '3333333'
    assert condition.match_objects(user, segments)

    user['userId'] = '123456'
    assert not condition.match_objects(user, segments)


def test_string_does_not_contain():
    condition.objects = ['12345', '987654', '665544']
    condition.predicate = fp.StringPredicate.DOES_NOT_CONTAIN

    user['userId'] = '3333333'
    assert condition.match_objects(user, segments)

    user['userId'] = '12345'
    assert not condition.match_objects(user, segments)


def test_string_does_not_match_regex():
    condition.objects = ['0?(13|14|15|18)[0-9]{9}']
    condition.predicate = fp.StringPredicate.DOES_NOT_MATCH_REGEX

    user['userId'] = '2122121'
    assert condition.match_objects(user, segments)

    user['userId'] = '13797347245'
    assert not condition.match_objects(user, segments)


def test_segmenting_is_in():
    condition.type = fp.ConditionType.SEGMENT
    condition.objects = ['test_project$test_segment']
    condition.predicate = fp.SegmentPredicate.IS_IN

    user['userId'] = '1'
    assert condition.match_objects(user, segments)

    user['userId'] = '3'
    assert not condition.match_objects(user, segments)


def test_segmenting_is_not_in():
    condition.type = fp.ConditionType.SEGMENT
    condition.objects = ['test_project$test_segment']
    condition.predicate = fp.SegmentPredicate.IS_NOT_IN

    user['userId'] = '3'
    assert condition.match_objects(user, segments)

    user['userId'] = '1'
    assert not condition.match_objects(user, segments)


def test_datetime_after():
    condition.type = fp.ConditionType.DATETIME
    condition.objects = [str(int(time.time() * 1000))]
    condition.predicate = fp.DatetimePredicate.AFTER

    user['userId'] = str(int(time.time() * 1000))
    assert condition.match_objects(user, segments)

    user['userId'] = str(int(time.time() * 1000) + 1)
    assert condition.match_objects(user, segments)

    del user['userId']
    assert not condition.match_objects(user, segments)

    user['userId'] = '1000'
    assert not condition.match_objects(user, segments)


def test_datetime_before():
    condition.type = fp.ConditionType.DATETIME
    condition.objects = [str(int(time.time() * 1000))]
    condition.predicate = fp.DatetimePredicate.BEFORE

    user['userId'] = str(int(time.time() * 1000) - 2)
    assert condition.match_objects(user, segments)

    user['userId'] = str(int(time.time() * 1000) + 1)
    assert not condition.match_objects(user, segments)

    user['userId'] = 'invalid datetime'
    assert not condition.match_objects(user, segments)


def test_number_equal():
    condition.type = fp.ConditionType.NUMBER
    condition.objects = ['12', '10.1']
    condition.predicate = fp.NumberPredicate.EQUAL

    user['userId'] = '  12.00000000 \n '
    assert condition.match_objects(user, segments)

    user['userId'] = '10.10\t '
    assert condition.match_objects(user, segments)

    user['userId'] = 'foo.bar+1'
    assert not condition.match_objects(user, segments)

    user['userId'] = ' '
    assert not condition.match_objects(user, segments)


def test_number_not_equal():
    condition.type = fp.ConditionType.NUMBER
    condition.objects = ['12', '16']
    condition.predicate = fp.NumberPredicate.NOT_EQUAL

    user['userId'] = '  13.00000000 \n '
    assert condition.match_objects(user, segments)

    user['userId'] = '  16.e0'
    assert not condition.match_objects(user, segments)

    user['userId'] = 'foo'
    assert not condition.match_objects(user, segments)

    condition.objects = ['foo', '16']
    user['userId'] = '1'
    assert not condition.match_objects(user, segments)


def test_number_greater_than():
    condition.type = fp.ConditionType.NUMBER
    condition.objects = ['12']
    condition.predicate = fp.NumberPredicate.GREATER_THAN

    user['userId'] = '  13 \n '
    assert condition.match_objects(user, segments)

    user['userId'] = '  11.999998e0'
    assert not condition.match_objects(user, segments)

    user['userId'] = '12.0'
    assert not condition.match_objects(user, segments)


def test_number_greater_or_equal():
    condition.type = fp.ConditionType.NUMBER
    condition.objects = ['12']
    condition.predicate = fp.NumberPredicate.GREATER_OR_EQUAL

    user['userId'] = '  13 \n '
    assert condition.match_objects(user, segments)

    user['userId'] = '12.0'
    assert condition.match_objects(user, segments)

    user['userId'] = '11.99999999999998'
    assert not condition.match_objects(user, segments)


def test_number_less_than():
    condition.type = fp.ConditionType.NUMBER
    condition.objects = ['17']
    condition.predicate = fp.NumberPredicate.LESS_THAN

    user['userId'] = '  13 \n '
    assert condition.match_objects(user, segments)

    user['userId'] = ' \t 18.999998e0'
    assert not condition.match_objects(user, segments)

    user['userId'] = '1.7e1'
    assert not condition.match_objects(user, segments)


def test_number_less_or_equal():
    condition.type = fp.ConditionType.NUMBER
    condition.objects = ['17']
    condition.predicate = fp.NumberPredicate.LESS_OR_EQUAL

    user['userId'] = '  13 \n '
    assert condition.match_objects(user, segments)

    user['userId'] = '17'
    assert condition.match_objects(user, segments)

    user['userId'] = '18'
    assert not condition.match_objects(user, segments)


def test_semver_equal():
    condition.type = fp.ConditionType.SEMVER
    condition.objects = ['1.1.3', '1.1.5']
    condition.predicate = fp.SemverPredicate.EQUAL

    user['userId'] = '1.1.3'
    assert condition.match_objects(user, segments)

    user['userId'] = '1.1.3+build.0001'
    assert condition.match_objects(user, segments)

    user['userId'] = '1.1.5'
    assert condition.match_objects(user, segments)

    user['userId'] = '1.1.5-beta'
    assert not condition.match_objects(user, segments)

    user['userId'] = ''
    assert not condition.match_objects(user, segments)

    del user['userId']
    assert not condition.match_objects(user, segments)


def test_semver_not_equal():
    condition.type = fp.ConditionType.SEMVER
    condition.objects = ['1.1.0', '1.2.0']
    condition.predicate = fp.SemverPredicate.NOT_EQUAL

    user['userId'] = '1.3.0'
    assert condition.match_objects(user, segments)

    user['userId'] = '1.1.0'
    assert not condition.match_objects(user, segments)

    user['userId'] = '1.2.0'
    assert not condition.match_objects(user, segments)


def test_semver_greater_than():
    condition.type = fp.ConditionType.SEMVER
    condition.objects = ['1.1.0', '1.2.0']
    condition.predicate = fp.SemverPredicate.GREATER_THAN

    user['userId'] = '1.1.1-rc1'
    assert condition.match_objects(user, segments)

    user['userId'] = '1.1.0-alpha'
    assert not condition.match_objects(user, segments)

    user['userId'] = '1.0.0'
    assert not condition.match_objects(user, segments)


def test_semver_greater_or_equal():
    condition.type = fp.ConditionType.SEMVER
    condition.objects = ['1.1.0', '1.2.0']
    condition.predicate = fp.SemverPredicate.GREATER_OR_EQUAL

    user['userId'] = '1.1.1'
    assert condition.match_objects(user, segments)

    user['userId'] = '1.1.0'
    assert condition.match_objects(user, segments)

    user['userId'] = '1.0.0'
    assert not condition.match_objects(user, segments)


def test_semver_less_than():
    condition.type = fp.ConditionType.SEMVER
    condition.objects = ['1.1.0', '1.2.0']
    condition.predicate = fp.SemverPredicate.LESS_THAN

    user['userId'] = '0.1.0'
    assert condition.match_objects(user, segments)

    user['userId'] = '1.1.7'
    assert condition.match_objects(user, segments)

    user['userId'] = '1.2.0'
    assert not condition.match_objects(user, segments)


def test_semver_less_or_equal():
    condition.type = fp.ConditionType.SEMVER
    condition.objects = ['1.1.0', '1.2.0']
    condition.predicate = fp.SemverPredicate.LESS_OR_EQUAL

    user['userId'] = '1.0.1'
    assert condition.match_objects(user, segments)

    user['userId'] = '1.2.0'
    assert condition.match_objects(user, segments)

    user['userId'] = '1.2.7'
    assert not condition.match_objects(user, segments)
