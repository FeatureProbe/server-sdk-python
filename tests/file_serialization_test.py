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

import featureprobe as fp


def test_local_mode_synchronizer():
    config = fp.Config(
        sync_mode='file',
        location='tests/resources/datasource/repo.json')
    feature_probe = fp.Client(
        server_sdk_key='server-61db54ecea79824cae3ac38d73f1961d698d0477',
        config=config)
    repo = feature_probe._data_repo
    assert len(repo.get_all_toggle()) > 0
    assert len(repo.get_all_segment()) > 0
