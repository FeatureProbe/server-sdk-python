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


from typing import TYPE_CHECKING

from featureprobe.hit_result import HitResult

if TYPE_CHECKING:
    from featureprobe.model.split import Split
    from featureprobe.user import User


class Serve:
    def __init__(self,
                 select: int,
                 split: "Split"):
        self._select = select
        self._split = split

    @classmethod
    def from_json(cls, json: dict):
        select = json.get('select', 0)
        split = json.get('split')
        if split is not None:
            split = Split.from_json(split)
        return cls(select, split)

    @property
    def select(self) -> int:
        return self._select

    @select.setter
    def select(self, value: int):
        self._select = value

    @property
    def split(self) -> "Split":
        return self._split

    @split.setter
    def split(self, value: "Split"):
        self._split = value

    def eval_index(self, user: "User", toggle_key: str) -> HitResult:
        if self._select:
            return HitResult(hit=True, index=self._select)

        return self._split.find_index(user, toggle_key)
