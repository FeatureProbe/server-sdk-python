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

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from featureprobe.user import User

class Event:
    def __init__(self, kind: str, created_time: int, user: "User"):
        self._created_time = created_time
        self._user = user
        self._kind = kind

    def to_dict(self) -> dict:
        return {
            'kind': self.kind,
            'time': self._created_time,
            'user': self._user.key
        }

    @property
    def created_time(self) -> int:
        return self._created_time

    @property
    def user(self) -> "User":
        return self._user

    @property
    def kind(self) -> str:
        return self._kind

class AccessEvent(Event):
    def __init__(
            self,
            timestamp: int,
            user: "User",
            key: str,
            value: object,
            version: int,
            variation_index: int,
            rule_index: int,
            reason: str,
            track_access_events: bool):
        super().__init__("access", timestamp, user)
        self._key = key
        self._value = value
        self._version = version
        self._variation_index = variation_index
        self._rule_index = rule_index
        self._reason = reason
        self._track_access_events = track_access_events

    def to_dict(self) -> dict:
        values = super().to_dict()
        values.update({
            'key': self._key,
            'value': self._value,
            'version': self._version,
            'variationIndex': self._variation_index,
            'ruleIndex': self._rule_index,
            'reason': self._reason
        })
        return values

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
    def variation_index(self):
        return self._variation_index

    @property
    def rule_index(self):
        return self._rule_index

    @property
    def reason(self):
        return self._reason

    @property
    def track_access_events(self):
        return self._track_access_events

class CustomEvent(Event):
    def __init__(self, timestamp: int, user: "User", name: str, value: Optional[float] = None):
        super().__init__("custom", timestamp, user)
        self._name = name
        self._value = value

    def to_dict(self) -> dict:
        values = super().to_dict()
        values['name'] = self._name
        if self._value is not None:
            values['value'] = self._value
        return values

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value