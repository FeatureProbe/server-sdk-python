from typing import List


class Distribution:
    def __init__(self, distribution: List[List[int]]):
        self._distribution = distribution or []

    @property
    def distribution(self):
        return self._distribution
