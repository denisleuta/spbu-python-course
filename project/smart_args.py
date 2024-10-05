import copy
import inspect
from functools import wraps


class Isolated:
    pass


class Evaluated:
    def __init__(self, func):
        assert callable(func), "Evaluated requires a function without arguments"
        self.func = func


def smart_args(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_spec = inspect.getfullargspec(func)

        # Handling named arguments with Isolated and Evaluated
        for name, default in func_spec.kwonlydefaults.items():
            if name not in kwargs:
                if isinstance(default, Isolated):
                    kwargs[name] = copy.deepcopy(kwargs[name])
                elif isinstance(default, Evaluated):
                    kwargs[name] = default.func()
                else:
                    kwargs[name] = default

        return func(*args, **kwargs)

    return wrapper
