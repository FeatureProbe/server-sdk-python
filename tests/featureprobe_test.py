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


import json
import logging

import pytest

import featureprobe as fp

# DON'T CARE: warnings about http connection error (pool syncer)
logging.basicConfig(level=logging.CRITICAL)


def setup_function():
    global test_cases  # noqa
    with open('resources/test/server-sdk-specification/spec/toggle_simple_spec.json', 'r', encoding='utf-8') as f:
        test_cases = json.load(f)


def test_empty_sdk_key():
    with pytest.raises(ValueError):
        fp.Server('')  # should not allow empty sdk key

    with pytest.raises(ValueError):
        fp.Server('  \n\t  ')  # should not allow empty sdk key

    try:
        fp.Server('foo')
    except Exception:  # noqa
        pytest.fail('ctor should not fail with not empty sdk key')


def test_case():
    tests = test_cases['tests']
    for scenario in tests:
        name = scenario['scenario']
        fixture = scenario['fixture']

        repo = fp.Repository.from_json(fixture)
        data_repo = fp.MemoryDataRepository(None, False, 0)  # noqa
        data_repo.refresh(repo)

        server = fp.Server('test_sdk_key')
        server._data_repo = data_repo

        cases = scenario['cases']
        for case in cases:
            case_name = case['name']
            # sourcery skip: replace-interpolation-with-fstring
            print('start executing scenario [%s] case [%s]' % (name, case_name))

            user_case = case['user']
            custom_values = user_case['customValues']
            attrs = {cv['key']: cv['value'] for cv in custom_values}
            user = fp.User(user_case['key'])
            user.attrs = attrs

            func_case = case['function']
            func_name = func_case['name']

            toggle_key = func_case['toggle']
            expect_result = case['expectResult']
            default_value = func_case['default']
            expect_value = expect_result['value']

            if func_name.endswith('value'):
                assert server.evaluate(toggle_key, user, default_value) == expect_value
            elif func_name.endswith('detail'):
                detail = server.evaluate_detail(toggle_key, user, default_value)
                assert detail.value == expect_value
                # assert detail.reason == expect_result['reason']
                # assert detail.version == expect_result['version']
                # assert (detail.rule_index is None) == expect_result['no_rule_index']
            else:
                pytest.fail('should have no other cases yet')
