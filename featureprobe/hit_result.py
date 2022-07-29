class HitResult:
    def __init__(self, hit: bool, index: int = None, reason: str = None):
        self._hit = hit
        self._index = index
        self._reason = reason

    @property
    def hit(self):
        return self._hit

    @property
    def index(self):
        return self._index

    @property
    def reason(self):
        return self._reason
