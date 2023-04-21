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

from featureprobe.polling_synchronizer import PollingSynchronizer
from featureprobe.memory_data_repository import MemoryDataRepository
from featureprobe.config import Config
from featureprobe.context import Context
from threading import Event
from requests import Session
from unittest.mock import patch


def test_init_synchronizer_failed():
    realy = Event()
    context = Context("test-sdk-key", Config())
    synchroizer = PollingSynchronizer.from_context(
        context, MemoryDataRepository.from_context(context), realy)
    realy.wait(2)

    assert not synchroizer.initialized()


@patch.object(Session, 'get')
def test_init_synchronizer_wait_for_init_success(session_get):
    realy = Event()
    context = Context("test-sdk-key", Config())
    session_get.return_value = MockHttpReponse(200, '{}')
    synchroizer = PollingSynchronizer.from_context(
        context, MemoryDataRepository.from_context(context), realy)
    synchroizer.sync()
    realy.wait(5)

    assert synchroizer.initialized()


class MockHttpReponse:
    def __init__(self, status_code, json_response):
        self.status_code = status_code
        self.response = json_response

    def raise_for_status(self):
        pass

    def json(self):
        return self.response
