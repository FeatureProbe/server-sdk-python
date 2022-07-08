import logging

from data_repository import DataRepository
from model.repository import Repository
from synchronizer import Synchronizer
import pkg_resources


class FileSynchronizer(Synchronizer):
    __logger = logging.getLogger('FeatureProbe-Synchronizer')
    __DEFAULT_LOCATION = 'datasource/repo.json'

    def __init__(self,
                 data_repository: DataRepository,
                 location='datasource/repo.json'):
        self._data_repository = data_repository
        self._location = location

    def sync(self):
        try:
            data = pkg_resources.resource_string(__name__, self._location).decode('utf-8')
        except FileNotFoundError as e:
            FileSynchronizer.__logger.error('repository file resource not found in path: %s' % self._location)
            data = ''
        # TODO: @classmethod ..
        repo = Repository.from_json(data)
        self._data_repository.refresh(repo)

    def close(self):
        return
