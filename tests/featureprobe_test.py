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

import json
import logging
import re
import time
from threading import Thread
import socket
from contextlib import closing
from requests import Session
import socketio
import eventlet
import pytest
from unittest.mock import patch

import featureprobe as fp
from featureprobe.memory_data_repository import MemoryDataRepository
from featureprobe.model import Repository

from commons import MockHttpReponse, find_free_port


# DON'T CARE: warnings about http connection error (pool syncer)
# logging.basicConfig(level=logging.CRITICAL)


def setup_function():
    global test_cases  # noqa
    with open(
        "tests/resources/test/server-sdk-specification/spec/toggle_simple_spec.json",
        "r",
        encoding="utf-8",
    ) as f:
        test_cases = json.load(f)


# def test_empty_sdk_key():
#     with pytest.raises(ValueError):
#         fp.Client('')  # should not allow empty sdk key
#
#     with pytest.raises(ValueError):
#         fp.Client('  \n\t  ')  # should not allow empty sdk key
#
#     try:
#         fp.Client('foo')
#     except Exception:  # noqa
#         pytest.fail('ctor should not fail with not empty sdk key')


# def test_case():
#     tests = test_cases['tests']
#     for scenario in tests:
#         name = scenario['scenario']
#         fixture = scenario['fixture']
#
#         repo = Repository.from_json(fixture)
#         data_repo = MemoryDataRepository(None, False, 0)  # noqa
#         data_repo.refresh(repo)
#
#         server = fp.Client('test_sdk_key')
#         server._data_repo = data_repo
#
#         cases = scenario['cases']
#         for case in cases:
#             case_name = case['name']
#             # sourcery skip: replace-interpolation-with-fstring
#             print(
#                 'start executing scenario [%s] case [%s]' %
#                 (name, case_name))
#
#             user_case = case['user']
#             custom_values = user_case['customValues']
#             attrs = {cv['key']: cv['value'] for cv in custom_values}
#             user = fp.User().stable_rollout(user_case['key'])
#             user.attrs = attrs
#
#             func_case = case['function']
#             func_name = func_case['name']
#
#             toggle_key = func_case['toggle']
#             expect_result = case['expectResult']
#             default_value = func_case['default']
#             expect_value = expect_result['value']
#
#             if func_name.endswith('value'):
#                 assert server.value(
#                     toggle_key, user, default_value) == expect_value
#             elif func_name.endswith('detail'):
#                 detail = server.value_detail(
#                     toggle_key, user, default_value)
#                 assert detail.value == expect_value
#                 if expect_result.get('reason') is not None:
#                     assert re.search(
#                         expect_result.get('reason'),
#                         detail.reason,
#                         re.IGNORECASE)
#             else:
#                 pytest.fail('should have no other cases yet')


def test_realtime_toggle_update(requests_mock):
    sio_server = socketio.Server()

    @sio_server.event
    def connect(sid, environ):
        print("sio client connected", sid, environ)

    @sio_server.event
    def disconnect(sid):
        print("sio client disconnected", sid)

    sio_server_app = socketio.WSGIApp(sio_server)
    server_port = find_free_port()
    Thread(
        target=lambda: eventlet.wsgi.server(
            eventlet.listen(("", server_port)), sio_server_app
        ),
        daemon=True,
    )

    requests_mock.get(
        "http://localhost:1234/api/server-sdk/toggles",
        text="{}")

    fp_client = fp.Client(
        "sdk key",
        fp.Config(
            remote_uri="http://localhost:1234",
            realtime_url="http://0.0.0.0:63851"),
    )
    assert fp_client._socket is not None
