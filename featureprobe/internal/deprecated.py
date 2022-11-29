import warnings


def _nameof(anything):
    if callable(anything):
        return "function<{}>".format(anything.__name__)
    elif type(anything) == property:
        return "property<{}>".format(anything.fget.__name__)
    # TODO: add more type support
    else:
        return None


def deprecated(*, since: str = None, successor=None):
    """Marks functions as deprecated."""

    def wrapper(func):
        def inner(*args, **kwargs):
            successor_name = _nameof(successor)
            warnings.warn(
                "{} is deprecated{}{}".format(
                    _nameof(func),
                    " since " + since if since is not None else "",
                    ", consider using {} instead.".format(successor_name)
                    if successor_name is not None
                    else "",
                ),
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        return inner

    return wrapper
