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

import json
import logging
from typing import TYPE_CHECKING

from featureprobe.model.repository import Repository
from featureprobe.synchronizer import Synchronizer

if TYPE_CHECKING:
    from featureprobe.context import Context
    from featureprobe.data_repository import DataRepository


class FileSynchronizer(Synchronizer):
    _logger = logging.getLogger('FeatureProbe-Synchronizer')

    def __init__(self,
                 data_repository: "DataRepository",
                 location: str):
        self._data_repository = data_repository
        self._location = location

    @classmethod
    def from_context(
            cls,
            context: "Context",
            data_repo: "DataRepository") -> "Synchronizer":
        return cls(data_repo, context.location)

    def sync(self):
        try:
            with open(self._location, 'r', encoding='utf-8') as f:
                repo = Repository.from_json(json.load(f))
                self._data_repository.refresh(repo)
        except FileNotFoundError:
            # sourcery skip: replace-interpolation-with-fstring
            self._logger.error(
                'repository file resource not found in path: %s' %
                self._location)

    def close(self):
        return
