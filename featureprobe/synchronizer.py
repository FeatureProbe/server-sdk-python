from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from featureprobe.context import Context
    from featureprobe.data_repository import DataRepository


class Synchronizer(ABC):

    @classmethod
    @abstractmethod
    def from_context(cls, context: "Context", data_repo: "DataRepository") -> "Synchronizer":
        pass

    @abstractmethod
    def sync(self):
        pass

    @abstractmethod
    def close(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
