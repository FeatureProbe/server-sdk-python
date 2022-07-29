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

from datetime import timedelta
from typing import Union

from requests.adapters import HTTPAdapter

from featureprobe.internal.defaultable import defaultable


@defaultable
class HttpConfig:
    def __init__(self,
                 pool_connections: int = 5,
                 pool_maxsize: int = 10,
                 conn_timeout: Union[timedelta, float] = timedelta(seconds=3),
                 read_timeout: Union[timedelta, float] = timedelta(seconds=3)):
        self.conn_timeout = conn_timeout.total_seconds() \
            if isinstance(conn_timeout, timedelta) \
            else conn_timeout
        self.read_timeout = read_timeout.total_seconds() \
            if isinstance(read_timeout, timedelta) \
            else read_timeout
        self.adapter = HTTPAdapter(
            pool_maxsize=pool_maxsize,
            pool_connections=pool_connections,
            max_retries=0,
        )
