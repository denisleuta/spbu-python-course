import copy
import inspect
from functools import wraps


class Evaluated:
    def __init__(self, func):
        self.func = func

    def __call__(self):
        return self.func()


class Isolated:
    pass


def smart_args(enable_positional=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_spec = inspect.getfullargspec(func)
            arg_names = func_spec.args
            defaults = func_spec.defaults or []
            default_offset = len(arg_names) - len(defaults)

            bound_arguments = {}
            if enable_positional:
                for idx, value in enumerate(args):
                    if idx < len(arg_names):
                        bound_arguments[arg_names[idx]] = value

            bound_arguments.update(kwargs)

            for i, name in enumerate(arg_names):
                if name not in bound_arguments:
                    if i >= default_offset:
                        default_value = defaults[i - default_offset]

                        if isinstance(default_value, Evaluated):
                            bound_arguments[name] = default_value()
                        elif isinstance(default_value, Isolated):
                            raise ValueError(
                                f"Argument '{name}' must be provided and cannot use Isolated."
                            )
                        else:
                            bound_arguments[name] = copy.deepcopy(default_value)

            func_args = [bound_arguments.get(arg, None) for arg in arg_names]
            return func(*func_args)

        return wrapper

    return decorator
