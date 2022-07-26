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


import featureprobe as fp


def setup_function():
    global split, user  # noqa
    split = fp.Split([
        [[0, 5000]],
        [[5000, 10000]],
    ], None, None)  # noqa
    user = fp.User('test_user_key')


def test_get_user_group():
    common_index = split.find_index(user, 'test_toggle_key')
    assert common_index.index == 0

    split.bucket_by = 'email'
    split.salt = 'abcddeafasde'
    user['email'] = 'test@gmail.com'
    custom_index = split.find_index(user, 'test_toggle_key')
    assert custom_index.index == 1
