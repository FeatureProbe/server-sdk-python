def defaultable(cls):
    _defaults = {}

    def check_or_create(*args, **kwargs):
        if args or kwargs:
            return cls(*args, **kwargs)
        if cls not in _defaults:
            default = cls()
            _defaults[cls] = default
            return default
        return _defaults[cls]

    return check_or_create
