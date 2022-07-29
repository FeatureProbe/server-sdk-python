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
