from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from featureprobe.user import User


class Event:
    def __init__(self, created_time: int, user: "User"):
        self._created_time = created_time
        self._user = user

    @property
    def created_time(self) -> int:
        return self._created_time

    @property
    def user(self) -> "User":
        return self._user


class AccessEvent(Event):
    def __init__(self, timestamp: int, user: "User", key: str, value: str, version: int, index: int):
        super().__init__(timestamp, user)
        self._key = key
        self._value = value
        self._version = version
        self._index = index

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @property
    def version(self):
        return self._version

    @property
    def index(self):
        return self._index
