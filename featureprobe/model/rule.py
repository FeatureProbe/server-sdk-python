from typing import List, Dict, TYPE_CHECKING

from featureprobe.hit_result import HitResult
from featureprobe.internal.json_decoder import json_decoder
from featureprobe.model.condition import Condition, ConditionType
from featureprobe.model.serve import Serve

if TYPE_CHECKING:
    from featureprobe.model.segment import Segment
    from featureprobe.user import User


class Rule:
    def __init__(self,
                 serve: "Serve" = None,
                 conditions: List["Condition"] = None):
        self._serve = serve
        self._conditions = conditions or []

    @classmethod
    @json_decoder
    def from_json(cls, json: dict) -> "Rule":
        serve = Serve.from_json(json.get('serve'))
        conditions = [Condition.from_json(c) for c in json.get('conditions', [])]
        return cls(serve, conditions)

    @property
    def serve(self) -> "Serve":
        return self._serve

    @serve.setter
    def serve(self, value: "Serve"):
        self._serve = value

    @property
    def conditions(self) -> List["Condition"]:
        return self._conditions

    @conditions.setter
    def conditions(self, value: List["Condition"]):
        self._conditions = value or []

    def hit(self, user: "User", segments: Dict[str, "Segment"], toggle_key: str) -> HitResult:
        for condition in self._conditions:
            if condition.type not in (ConditionType.SEGMENT, ConditionType.DATETIME) \
                    and not user.has_attr(condition.subject):
                return HitResult(hit=False,
                                 reason="Warning: User with key '%s' does not have attribute name '%s'"
                                        % (user.key, condition.subject))
            if not condition.match_objects(user, segments):
                return HitResult(hit=False)

        return self._serve.eval_index(user, toggle_key)
