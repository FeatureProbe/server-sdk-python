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

__version__ = '0.1.0'

# --------------- API --------------- #

from featureprobe.model import *

from featureprobe.access_recorder import (
    AccessCounter,
    AccessRecorder,
)

from featureprobe.config import Config
from featureprobe.context import Context
from featureprobe.data_repository import DataRepository
from featureprobe.detail import Detail
from featureprobe.evaluation_result import EvaluationResult
from featureprobe.event import AccessEvent
from featureprobe.hit_result import HitResult
from featureprobe.http_config import HttpConfig
from featureprobe.client import Client
from featureprobe.user import User


__all__ = [
    # featureprobe.model

    'Condition',
    'ConditionType',
    'StringPredicate',
    'SegmentPredicate',
    'DatetimePredicate',
    'NumberPredicate',
    'SemverPredicate',
    'Distribution',
    'Repository',
    'Rule',
    'Segment',
    'SegmentRule',
    'Serve',
    'Split',
    'Toggle',

    # featureprobe
    'AccessCounter',
    'AccessRecorder',
    'Client',
    'Config',
    'Context',
    'DataRepository',
    'Detail',
    'EvaluationResult',
    'AccessEvent',
    'HitResult',
    'HttpConfig',
    'User',
]
