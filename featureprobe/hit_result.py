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

class HitResult:
    def __init__(self, hit: bool, index: int = None, reason: str = None):
        self._hit = hit
        self._index = index
        self._reason = reason

    @property
    def hit(self):
        return self._hit

    @property
    def index(self):
        return self._index

    @property
    def reason(self):
        return self._reason
