from abc import ABCMeta, abstractmethod
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from featureprobe.context import Context
    from featureprobe.model.repository import Repository
    from featureprobe.model.toggle import Toggle


class DataRepository(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def from_context(cls, context: "Context") -> "DataRepository":
        pass

    @abstractmethod
    def refresh(self, repo: "Repository"):
        pass

    @abstractmethod
    def get_toggle(self, key: str) -> "Toggle":
        pass

    @abstractmethod
    def get_all_toggle(self) -> Dict[str, "Toggle"]:
        pass

    @abstractmethod
    def get_segment(self, key: str) -> "Toggle":
        pass

    @abstractmethod
    def get_all_segment(self) -> Dict[str, "Toggle"]:
        pass

    @property
    @abstractmethod
    def initialized(self) -> bool:
        pass

    @abstractmethod
    def close(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
