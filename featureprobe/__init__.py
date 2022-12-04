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

__author__ = 'FeatureProbe'
__license__ = 'Apache 2.0'


# PEP440 spec:
# [N!]N(.N)*[{a|b|rc}N][.postN][.devN]
__version__ = 'NO_MANUAL_MAINTENANCE_NEEDED'


# --------------- API --------------- #

import featureprobe.model

from featureprobe.config import Config
from featureprobe.detail import Detail
from featureprobe.http_config import HttpConfig
from featureprobe.client import Client
from featureprobe.user import User


__all__ = [
    'Client',
    'Config',
    'Detail',
    'HttpConfig',
    'User',
]
