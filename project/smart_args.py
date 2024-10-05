import copy
from functools import wraps
import inspect


class Isolated:
    pass


class Evaluated:
    def __init__(self, func):
        assert callable(func), "Evaluated requires a function with no arguments"
        self.func = func


import inspect
from functools import wraps


def smart_args(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_spec = inspect.getfullargspec(func)

        if func_spec.kwonlydefaults:
            for name, default in func_spec.kwonlydefaults.items():
                if name not in kwargs:
                    kwargs[name] = default

        return func(*args, **kwargs)

    return wrapper
