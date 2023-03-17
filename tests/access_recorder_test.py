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


def _timestamp():
    return int(time.time() * 1000)


def setup_function():
    global recorder, event  # noqa
    recorder = fp.AccessSummaryRecorder()
    user = fp.User().stable_rollout('test_user')
    event = fp.AccessEvent(_timestamp(), user,
                           key='test_toggle', value='true',
                           version=1,
                           variation_index=1,
                           rule_index=0,
                           track_access_events=True,
                           reason='')


def test_add_event():
    recorder.add(event)
    assert recorder.start_time > 0
    assert recorder.end_time == 0
    assert recorder.counters.get('test_toggle')[0].value == 'true'
    assert recorder.counters.get('test_toggle')[0].count == 1
    assert recorder.counters.get('test_toggle')[0].version == 1
    assert recorder.counters.get('test_toggle')[0].index == 1


def test_get_snapshot():
    recorder.add(event)
    snapshot = recorder.snapshot()
    assert len(snapshot.counters) == 1
    assert len(snapshot.counters.get('test_toggle')) == 1
