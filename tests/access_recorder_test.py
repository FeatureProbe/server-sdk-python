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


import time

import featureprobe as fp


def _timestamp():
    return int(time.time())


def setup_function():
    global recorder, event  # noqa
    recorder = fp.AccessRecorder()
    user = fp.User('test_user')
    event = fp.AccessEvent(_timestamp(), user,
                           key='test_toggle', value='true',
                           version=1, index=0)


def test_add_event():
    recorder.add(event)
    assert 0 < recorder.start_time
    assert 0 == recorder.end_time
    assert 'true' == recorder.counters.get('test_toggle')[0].value
    assert 1 == recorder.counters.get('test_toggle')[0].count
    assert 1 == recorder.counters.get('test_toggle')[0].version
    assert 0 == recorder.counters.get('test_toggle')[0].index
