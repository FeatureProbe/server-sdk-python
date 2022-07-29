from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from featureprobe.context import Context
    from featureprobe.event import Event


class EventProcessor(ABC):

    @classmethod
    @abstractmethod
    def from_context(cls, context: "Context") -> "EventProcessor":
        pass

    @abstractmethod
    def push(self, event: "Event"):
        pass

    @abstractmethod
    def flush(self):
        pass

    @abstractmethod
    def shutdown(self):
        pass
