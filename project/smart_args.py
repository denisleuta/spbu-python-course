import copy
from functools import wraps
import inspect


class Isolated:
    pass


class Evaluated:
    def __init__(self, func):
        assert callable(func), "Evaluated требует функцию без аргументов"
        self.func = func


def smart_args(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_spec = inspect.getfullargspec(func)

        for name, default in func_spec.kwonlydefaults.items():
            if name not in kwargs:
                if isinstance(default, Isolated):
                    kwargs[name] = copy.deepcopy(kwargs[name] if name in kwargs else {})
                elif isinstance(default, Evaluated):
                    kwargs[name] = default.func()
                else:
                    kwargs[name] = default

        return func(*args, **kwargs)

    return wrapper
