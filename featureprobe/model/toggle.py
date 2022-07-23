# -*- coding: UTF-8 -*-

# Copyright 2022 FeatureProbe
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from typing import List, Optional, Dict

from featureprobe.evaluation_result import EvaluationResult
from featureprobe.user import User
from featureprobe.model.rule import Rule
from featureprobe.model.segment import Segment
from featureprobe.model.serve import Serve
from featureprobe.hit_result import HitResult


class Toggle:
    def __init__(self):
        self._key = ''
        self._enabled = False
        self._version = 0
        self._disabled_serve = None  # Serve
        self._default_serve = None  # Serve
        self._rules = []  # List[Rule]
        self._variations = []
        self._for_client = False

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
    def disabled_serve(self) -> Serve:
        return self._disabled_serve

    @disabled_serve.setter
    def disabled_serve(self, value: Serve):
        self._disabled_serve = value

    @property
    def default_serve(self) -> Serve:
        return self._default_serve

    @default_serve.setter
    def default_serve(self, value: Serve):
        self._default_serve = value

    @property
    def rules(self) -> List[Rule]:
        return self._rules

    @rules.setter
    def rules(self, value: List[Rule]):
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

    def eval(self, user: User, segments: Dict[str, Segment], default_value) -> EvaluationResult:
        if not self._enabled:
            return self._create_disabled_result(user, self._key, default_value)

        warning = None

        for index, rule in enumerate(self._rules or []):
            hit_result = rule.hit(user, segments, self._key)
            if hit_result.hit:
                return self._hit_value(hit_result, default_value, index)
            warning = hit_result.reason or ''

        return self._create_default_result(user, self._key, default_value, warning)

    def _create_disabled_result(self, user: User, toggle_key: str, default_value):
        disabled_result = self._hit_value(self._disabled_serve.eval_index(user, toggle_key), default_value)
        disabled_result.reason = 'Toggle disabled'
        return disabled_result

    def _create_default_result(self, user: User, toggle_key: str, default_value, warning: str) -> EvaluationResult:
        # sourcery skip: replace-interpolation-with-fstring
        default_result = self._hit_value(self._default_serve.eval_index(user, toggle_key), default_value)
        default_result.reason = 'Default rule hit. %s' % warning
        return default_result

    def _hit_value(self, hit_result: HitResult, default_value, rule_index: Optional[int] = None) -> EvaluationResult:
        res = EvaluationResult(default_value, rule_index, hit_result.index, self._version, hit_result.reason or '')
        if hit_result.index is not None:
            variation = self._variations[hit_result.index]
            if isinstance(variation, int) and isinstance(default_value, float):
                res.value = float(variation)
            else:
                res.value = variation
            if rule_index is not None:
                res.reason = 'Rule %d hit' % rule_index

        return res
