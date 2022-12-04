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

import sys

from featureprobe.pooling_synchronizer import PoolingSynchronizer
from featureprobe.memory_data_repository import MemoryDataRepository
from featureprobe.realtime import RealtimeToggleUpdateNS
from featureprobe.config import Config
from featureprobe.context import Context
from threading import Event
from requests import Session
from unittest.mock import patch


class MockHttpResponse:
    def __init__(self, status_code, json_response):
        self.status_code = status_code
        self.response = json_response

    def raise_for_status(self):
        pass

    def json(self):
        return self.response


def test_init_synchronizer_failed():
    ready = Event()
    context = Context("test-sdk-key", Config())
    synchronizer = PoolingSynchronizer.from_context(
        context, MemoryDataRepository.from_context(context), ready)
    ready.wait(2)

    assert not synchronizer.initialized()


@patch.object(Session, 'get')
def test_init_synchronizer_wait_for_init_success(session_get):
    ready = Event()
    context = Context("test-sdk-key", Config())
    session_get.return_value = MockHttpResponse(200, '{}')
    synchronizer = PoolingSynchronizer.from_context(
        context, MemoryDataRepository.from_context(context), ready)
    synchronizer.start()
    ready.wait(5)

    assert synchronizer.initialized()


@patch.object(Session, 'get')
def test_realtime_toggle_update(session_get):
    ready = Event()
    context = Context("test-sdk-key", Config(refresh_interval=10000))
    repo = MemoryDataRepository.from_context(context)
    synchronizer = PoolingSynchronizer.from_context(context, repo, ready)
    sio = RealtimeToggleUpdateNS(None, context, synchronizer)

    session_get.return_value = MockHttpResponse(200, '{}')
    synchronizer.start()
    ready.wait(5)

    assert synchronizer.initialized()
    assert not repo.get_all_toggle() and not repo.get_all_segment()

    with open('tests/resources/datasource/repo.json') as f:
        session_get.return_value = MockHttpResponse(200, f.read())
    sio.on_update(None)

    assert repo.get_all_toggle() and repo.get_all_segment()

