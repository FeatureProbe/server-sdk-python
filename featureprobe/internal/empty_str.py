from typing import Optional


def empty_str(s: Optional[str]):
    return True if s is None else not bool(s.strip())
