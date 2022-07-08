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

from fp_user import FPUser
from hit_result import HitResult
from split import Split


class Serve:
    def __init__(self,
                 select: int = 0,
                 split: Split = None):
        self._select = select
        self._split = split

    @property
    def select(self) -> int:
        return self._select

    @select.setter
    def select(self, select: int):
        self._select = select

    @property
    def split(self) -> Split:
        return self._split

    @split.setter
    def split(self, split: Split):
        self._split = split

    def eval_index(self, user: FPUser, toggle_key: str) -> HitResult:
        if self._select:
            return HitResult(True, self._select)

        return self._split.find_index(user, toggle_key)
