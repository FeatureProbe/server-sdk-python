from typing import Optional


class Detail:
    def __init__(self, value=None,
                 rule_index: Optional[int] = None,
                 version: Optional[int] = None,
                 reason: Optional[str] = None):
        self.value = value
        self.rule_index = rule_index
        self.version = version
        self.reason = reason

    def __str__(self):
        return "FPDetail{value=%s, rule_index=%s, version=%s, reason='%s'}" % \
               (self.value, self.rule_index, self.version, self.reason)
