from typing import Optional


class EvaluationResult:
    def __init__(self,
                 value,
                 rule_index: Optional[int],
                 variation_index: Optional[int],
                 version: int,
                 reason: str):
        self.value = value
        self.rule_index = rule_index
        self.variation_index = variation_index
        self.version = version
        self.reason = reason
