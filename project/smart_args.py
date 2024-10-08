import copy
import inspect
from functools import wraps


class Evaluated:
    """
    A class that wraps a function to delay its execution until called.

    This class is useful for creating default values for function parameters
    that should only be evaluated when the function is called, rather than
    when the function is defined.

    Parameters:
    ----------
    func : callable
        A function that will be evaluated when the instance is called.
    """

    def __init__(self, func):
        self.func = func

    def __call__(self):
        return self.func()


class Isolated:
    """
    A marker class used to indicate that a function argument should be treated as isolated.

    When used as a default value for a function parameter, it indicates that the argument
    should not be modified or shared outside the function. Instead, a deep copy of the
    argument will be created to ensure isolation.
    """

    pass


def smart_args(enable_positional=True):
    """
    A decorator that intelligently handles arguments, supporting both positional and keyword arguments.

    This decorator inspects the arguments passed to the decorated function, applies default
    values if necessary, and handles special cases for custom types such as `Evaluated`
    and `Isolated`. Optionally, it allows positional argument usage to be toggled on or off.

    Args:
        enable_positional (bool): If True, positional arguments are supported. If False, only
                                  keyword arguments are allowed. Default is True.

    Returns:
        function: The decorated function with enhanced argument handling.

    Raises:
        ValueError: If an argument marked with `Isolated` is not provided during the call.
    """

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
