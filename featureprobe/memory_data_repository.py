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

import time
from typing import Dict, Optional, TYPE_CHECKING

from featureprobe.data_repository import DataRepository
from featureprobe.model.repository import Repository

if TYPE_CHECKING:
    from featureprobe.context import Context
    from featureprobe.model.segment import Segment
    from featureprobe.model.toggle import Toggle


class MemoryDataRepository(DataRepository):
    def __init__(self,
                 data: Repository,
                 initialized: bool,
                 updated_timestamp: int):
        self._data = data
        self._initialized = initialized
        self._updated_timestamp = updated_timestamp

    @classmethod
    def from_context(cls, context: "Context") -> DataRepository:
        return cls(data=None, initialized=False, updated_timestamp=0)  # noqa

    def refresh(self, repo: Repository):
        if repo is not None \
                and repo.toggles is not None \
                and repo.segments is not None:
            self._data = Repository(repo.toggles.copy(), repo.segments.copy())
            self._initialized = True
            self._updated_timestamp = int(time.time() * 1000)

    def get_toggle(self, key: str) -> Optional["Toggle"]:
        return self._data.toggles.get(key) if self._initialized else None

    def get_all_toggle(self) -> Dict[str, "Toggle"]:
        return self._data.toggles if self._initialized else {}

    def get_segment(self, key: str) -> Optional["Segment"]:
        return self._data.segments.get(key) if self._initialized else None

    def get_all_segment(self) -> Dict[str, "Toggle"]:
        return self._data.segments if self._initialized else {}

    def initialized(self) -> bool:
        return self._initialized

    def close(self):
        self._data = None
