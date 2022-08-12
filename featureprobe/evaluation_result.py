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

from typing import Optional


class EvaluationResult:
    def __init__(self,
                 value,
                 rule_index: Optional[int],
                 variation_index: Optional[int],
                 version: int,
                 reason: str):
        self.value = value
        self.rule_index = rule_index
        self.variation_index = variation_index
        self.version = version
        self.reason = reason
