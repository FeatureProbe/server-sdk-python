import time
from typing import Dict

from context import Context
from data_repository import DataRepository
from model.repository import Repository
from model.toggle import Toggle


class MemoryDataRepository(DataRepository):
    def __init__(self):
        self._data = None  # Repository
        self._initialized = False
        self._updated_timestamp = 0

    @classmethod
    def from_context(cls, context: Context):
        return cls()

    def refresh(self, repo: Repository):
        if repo and repo.toggles and repo.segments:
            self._data = Repository(repo.toggles.copy(), repo.segments.copy())
            self._initialized = True
            self._updated_timestamp = int(time.time())

    def get_toggle(self, key: str) -> Toggle:
        return self._data.toggles.get(key) if self._initialized else None

    def get_all_toggle(self) -> Dict[str, Toggle]:
        return self._data.toggles if self._initialized else {}

    def get_segment(self, key: str) -> Toggle:
        return self._data.segments.get(key) if self._initialized else None

    def get_all_segment(self) -> Dict[str, Toggle]:
        return self._data.segments if self._initialized else {}

    def initialized(self) -> bool:
        return self._initialized

    def close(self):
        return
