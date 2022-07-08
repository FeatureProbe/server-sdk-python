import time
from typing import Dict

from data_repository import DataRepository
from model.repository import Repository
from model.toggle import Toggle


class MemoryDataRepository(DataRepository):
    def __init__(self):
        self._data = None  # Repository
        self._initialized = False
        self._updated_timestamp = 0

    def refresh(self, repo: Repository):
        if repo and repo.toggles and repo.segments:
            self._data = Repository(repo.toggles.copy(), repo.segments.copy())
            self._initialized = True
            self._updated_timestamp = int(time.time())

    def get_toggle(self, key: str) -> Toggle:
        if self._initialized:
            return self._data.toggles.get(key)
        return None

    def get_all_toggle(self) -> Dict[str, Toggle]:
        if self._initialized:
            return self._data.toggles
        return {}

    def get_segment(self, key: str) -> Toggle:
        if self._initialized:
            return self._data.segments.get(key)
        return None

    def get_all_segment(self) -> Dict[str, Toggle]:
        if self._initialized:
            return self._data.segments
        return {}

    def initialized(self) -> bool:
        return self._initialized

    def close(self):
        return
