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

from evaluation_result import EvaluationResult
from featureprobe.fp_user import FPUser
from model.rule import Rule
from model.segment import Segment
from serve import Serve
from hit_result import HitResult


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
    def key(self, key: str):
        self._key = key

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, enabled: bool):
        self._enabled = enabled

    @property
    def version(self) -> int:
        return self._version

    @version.setter
    def version(self, version: int):
        self._version = version

    @property
    def disabled_serve(self) -> Serve:
        return self._disabled_serve

    @disabled_serve.setter
    def disabled_serve(self, disabled_serve: Serve):
        self._disabled_serve = disabled_serve

    @property
    def default_serve(self) -> Serve:
        return self._default_serve

    @default_serve.setter
    def default_serve(self, default_serve: Serve):
        self._default_serve = default_serve

    @property
    def rules(self) -> List[Rule]:
        return self._rules

    @rules.setter
    def rules(self, rules: List[Rule]):
        self._rules = rules

    @property
    def variations(self) -> List[str]:
        return self._variations

    @variations.setter
    def variations(self, variations: List[str]):
        self._variations = variations

    @property
    def for_client(self) -> bool:
        return self._for_client

    @for_client.setter
    def for_client(self, for_client: bool):
        self._for_client = for_client

    def eval(self, user: FPUser, segments: Dict[str, Segment], default_value) -> EvaluationResult:
        if not self._enabled:
            return self.__create_disabled_result(user, self._key, default_value)

        warning = None

        for index, rule in enumerate(self._rules or []):
            hit_result = rule.hit(user, segments, self._key)
            if hit_result.hit:
                return self.__hit_value(hit_result, default_value, index)
            warning = hit_result.reason or ''

        return self.__create_default_result(user, self._key, default_value, warning)

    def __create_disabled_result(self, user: FPUser, toggle_key: str, default_value):
        disabled_result = self.__hit_value(self._disabled_serve.eval_index(user, toggle_key), default_value)
        disabled_result.reason = 'Toggle disabled'
        return disabled_result

    def __create_default_result(self, user: FPUser, toggle_key: str, default_value, warning: str) -> EvaluationResult:
        default_result = self.__hit_value(self._default_serve.eval_index(user, toggle_key), default_value)
        default_result.reason = 'Default rule hit. %s' % warning
        return default_result

    def __hit_value(self, hit_result: HitResult, default_value, rule_index: Optional[int] = None) -> EvaluationResult:
        res = EvaluationResult(default_value, rule_index, hit_result.index, self._version, hit_result.reason or '')
        if hit_result.index:
            variation = self._variations[hit_result.index]
            if isinstance(variation, int) and isinstance(default_value, float):
                res.value = float(variation)
            else:
                res.value = variation
            if rule_index:
                res.reason = 'Rule %d hit' % rule_index

        return res
