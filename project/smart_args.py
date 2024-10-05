import copy
import inspect
from functools import wraps


class Isolated:
    pass


class Evaluated:
    def __init__(self, func):
        self.func = func

    def __call__(self):
        return self.func()


def smart_args(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get the signature of the function
        sig = inspect.signature(func)
        bound_arguments = sig.bind_partial(*args, **kwargs)

        for name, param in sig.parameters.items():
            if name in bound_arguments.arguments:
                continue  # Argument is provided by the user

            default = param.default
            if isinstance(default, Evaluated):
                bound_arguments.arguments[name] = default()
            elif isinstance(default, Isolated):
                raise ValueError(
                    f"Argument '{name}' must be provided and cannot use Isolated."
                )
            elif isinstance(default, dict):  # Example for mutable types
                bound_arguments.arguments[name] = copy.deepcopy(default)

        return func(*bound_arguments.args, **bound_arguments.kwargs)

    return wrapper
