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

import os.path
import pathlib

timezone = os.environ.get('TZ')

if timezone is None:
    try:
        if os.path.exists('/etc/timezone'):
            timezone = pathlib.Path('/etc/timezone').read_text()
        else:
            timezone = 'Asia/Shanghai'
    except BaseException:
        timezone = 'Asia/Shanghai'
