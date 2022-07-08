def defaultable(cls):
    _defaults = {}

    def check_and_return(*args, **kwargs):
        if args or kwargs:
            return cls(*args, **kwargs)
        if cls not in _defaults:
            _defaults[cls] = cls()
        return _defaults[cls]

    return check_and_return
