import json


def json_decoder(func):
    def wrapper(cls, json_):
        if json_ is None:
            return None
        if isinstance(json_, dict):
            return func(cls, json_)

        return func(cls, json.loads(json_))

    return wrapper
