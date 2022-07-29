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

from typing import Dict

from featureprobe.internal.json_decoder import json_decoder
from featureprobe.model.segment import Segment
from featureprobe.model.toggle import Toggle


class Repository:
    def __init__(self,
                 toggles: Dict[str, "Toggle"] = None,
                 segments: Dict[str, "Segment"] = None):
        self._toggles = toggles or {}
        self._segments = segments or {}

    @classmethod
    @json_decoder
    def from_json(cls, json: dict) -> "Repository":
        toggles = json.get('toggles', {})
        segments = json.get('segments', {})
        return cls(
            toggles={k: Toggle.from_json(v) for k, v in toggles.items()},
            segments={k: Segment.from_json(v) for k, v in segments.items()}
        )

    @property
    def toggles(self) -> Dict[str, "Toggle"]:
        return self._toggles

    @toggles.setter
    def toggles(self, value: Dict[str, "Toggle"]):
        self._toggles = value or {}

    @property
    def segments(self) -> Dict[str, "Segment"]:
        return self._segments

    @segments.setter
    def segments(self, value: Dict[str, "Segment"]):
        self._segments = value or {}
