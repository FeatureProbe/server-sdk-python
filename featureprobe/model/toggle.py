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

from typing import List, Optional, Dict, TYPE_CHECKING

from featureprobe.evaluation_result import EvaluationResult
from featureprobe.internal.json_decoder import json_decoder
from featureprobe.model.rule import Rule
from featureprobe.model.serve import Serve

if TYPE_CHECKING:
    from featureprobe.hit_result import HitResult
    from featureprobe.model.segment import Segment
    from featureprobe.user import User


class Toggle:
    def __init__(self,
                 key: str,
                 enabled: bool,
                 version: int,
                 disabled_serve: "Serve",
                 default_serve: "Serve",
                 rules: List["Rule"],
                 variations: list,
                 for_client: bool):
        self._key = key
        self._enabled = enabled
        self._version = version
        self._disabled_serve = disabled_serve
        self._default_serve = default_serve
        self._rules = rules
        self._variations = variations
        self._for_client = for_client

    @classmethod
    @json_decoder
    def from_json(cls, json: dict) -> "Toggle":
        key = json.get('key')
        enabled = json.get('enabled', False)
        version = json.get('version', 1)
        disabled_serve = Serve.from_json(json.get('disabledServe'))
        default_serve = Serve.from_json(json.get('defaultServe'))
        rules = [Rule.from_json(r) for r in json.get('rules', [])]
        variations = json.get('variations', [])
        for_client = json.get('forClient', False)
        return cls(
            key,
            enabled,
            version,
            disabled_serve,
            default_serve,
            rules,
            variations,
            for_client)

    @property
    def key(self) -> str:
        return self._key

    @key.setter
    def key(self, value: str):
        self._key = value

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value

    @property
    def version(self) -> int:
        return self._version

    @version.setter
    def version(self, value: int):
        self._version = value

    @property
    def disabled_serve(self) -> "Serve":
        return self._disabled_serve

    @disabled_serve.setter
    def disabled_serve(self, value: "Serve"):
        self._disabled_serve = value

    @property
    def default_serve(self) -> "Serve":
        return self._default_serve

    @default_serve.setter
    def default_serve(self, value: "Serve"):
        self._default_serve = value

    @property
    def rules(self) -> List["Rule"]:
        return self._rules

    @rules.setter
    def rules(self, value: List["Rule"]):
        self._rules = value or []

    @property
    def variations(self) -> List[str]:
        return self._variations

    @variations.setter
    def variations(self, value: List[str]):
        self._variations = value or []

    @property
    def for_client(self) -> bool:
        return self._for_client

    @for_client.setter
    def for_client(self, value: bool):
        self._for_client = value

    def eval(self,
             user: "User",
             segments: Dict[str,
                            "Segment"],
             default_value: object) -> "EvaluationResult":
        if not self._enabled:
            return self._create_disabled_result(user, self._key, default_value)

        warning = None

        for index, rule in enumerate(self._rules or []):
            hit_result = rule.hit(user, segments, self._key)
            if hit_result.hit:
                return self._hit_value(hit_result, default_value, index)
            warning = hit_result.reason

        return self._create_default_result(
            user, self._key, default_value, warning)

    def _create_disabled_result(
            self,
            user: "User",
            toggle_key: str,
            default_value: object) -> "EvaluationResult":
        disabled_result = self._hit_value(
            self._disabled_serve.eval_index(
                user, toggle_key), default_value)
        disabled_result.reason = 'Toggle disabled'
        return disabled_result

    def _create_default_result(self, user: "User", toggle_key: str,
                               default_value: object,
                               warning: str) -> "EvaluationResult":
        default_result = self._hit_value(
            self._default_serve.eval_index(
                user, toggle_key), default_value)
        # sourcery skip: replace-interpolation-with-fstring
        default_result.reason = 'Default rule hit. %s' % warning
        return default_result

    def _hit_value(self, hit_result: "HitResult", default_value: object,
                   rule_index: Optional[int] = None) -> "EvaluationResult":
        res = EvaluationResult(
            default_value,
            rule_index,
            hit_result.index,
            self._version,
            hit_result.reason or '')
        if hit_result.index is not None:
            variation = self._variations[hit_result.index]
            if isinstance(variation, int) and isinstance(default_value, float):
                res.value = float(variation)
            else:
                res.value = variation
            if rule_index is not None:
                res.reason = 'Rule %d hit' % rule_index

        return res
