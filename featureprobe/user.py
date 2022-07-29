from typing import Dict


class User:
    def __init__(self, key: str, attrs: Dict[str, str] = None):
        self._key = key
        self._attrs = attrs or {}

    def __setitem__(self, key: str, value: str):
        self._attrs[key] = value

    def __getitem__(self, item: str):
        try:
            return self._attrs[item]
        except KeyError:
            return None

    def __delitem__(self, key: str):
        self._attrs.pop(key, None)

    @property
    def key(self) -> str:
        return self._key

    @property
    def attrs(self) -> Dict[str, str]:
        return self._attrs

    @attrs.setter
    def attrs(self, attrs: Dict[str, str]):
        self._attrs = attrs

    def with_attr(self, key: str, value: str):
        self._attrs[key] = value

    def has_attr(self, attr: str):
        return attr in self._attrs
