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
    def from_context(cls, context: "Context", data_repo: "DataRepository") -> "Synchronizer":
        return cls(data_repo, context.location)

    def sync(self):
        try:
            with open(self._location, 'r', encoding='utf-8') as f:
                repo = Repository.from_json(json.load(f))
                self._data_repository.refresh(repo)
        except FileNotFoundError:
            # sourcery skip: replace-interpolation-with-fstring
            self._logger.error('repository file resource not found in path: %s' % self._location)

    def close(self):
        return
