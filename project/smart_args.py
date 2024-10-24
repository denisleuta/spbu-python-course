import copy
import inspect
from functools import wraps
from typing import Any, Callable, List, Optional, Union, Dict


class Evaluated:
    """
    Delays the evaluation of a function until it's explicitly called.

    Args:
        func (Callable): The function to be evaluated later.
    """

    def __init__(self, func: Callable):
        self.func = func

    def __call__(self) -> Any:
        return self.func()


class Isolated:
    """
    Marks an argument as needing to be isolated by deep copying.
    Use this for arguments that should not share state with others.
    """

    pass


def smart_args(enable_positional: bool = True) -> Callable:
    """
    Decorator that handles arguments intelligently, applying default values
    and custom behavior for special cases such as `Evaluated` and `Isolated` types.

    Args:
        enable_positional (bool): If True, allows the use of positional arguments. Defaults to True.

    Returns:
        Callable: A decorated function with enhanced argument handling.
    """

    def decorator(func: Callable) -> Callable:
        func_spec = inspect.getfullargspec(func)
        arg_names: List[str] = func_spec.args
        kwonly_names: List[str] = func_spec.kwonlyargs  # Add for keyword-only arguments
        defaults: Optional[List[Union[Evaluated, Isolated, Any]]] = (
            list(func_spec.defaults) if func_spec.defaults is not None else []
        )
        kwonly_defaults: Dict[str, Any] = (
            func_spec.kwonlydefaults or {}
        )  # Use empty dictionary

        default_offset: int = (
            len(arg_names) - len(defaults) if defaults else len(arg_names)
        )

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            bound_arguments: Dict[str, Any] = {}

            # Handle positional arguments if enabled
            if enable_positional:
                for idx, value in enumerate(args):
                    if idx < len(arg_names):
                        if isinstance(value, Isolated):
                            raise ValueError(
                                f"Argument '{arg_names[idx]}' must be provided explicitly and cannot use Isolated."
                            )
                        bound_arguments[arg_names[idx]] = value
            else:
                if args:
                    raise TypeError(
                        f"Positional arguments are not allowed for {func.__name__}, please use keyword arguments."
                    )

            # Update with keyword arguments
            bound_arguments.update(kwargs)

            # Handle default values and special types like Evaluated and Isolated for normal args
            for i, name in enumerate(arg_names):
                if name not in bound_arguments:
                    if i >= default_offset and defaults is not None:
                        default_value = defaults[i - default_offset]
                        if isinstance(default_value, Evaluated):
                            bound_arguments[name] = default_value()
                        elif isinstance(default_value, Isolated):
                            raise ValueError(
                                f"Argument '{name}' must be provided explicitly and cannot use Isolated."
                            )
                        else:
                            bound_arguments[name] = copy.deepcopy(default_value)

            # Handle default values and special types for keyword-only arguments
            for name in kwonly_names:
                if name not in bound_arguments and name in kwonly_defaults:
                    bound_arguments[name] = kwonly_defaults[name]

            # Ensure all bound arguments are isolated
            for name, value in bound_arguments.items():
                if isinstance(value, Isolated):
                    raise ValueError(
                        f"Argument '{name}' must be provided explicitly and cannot use Isolated."
                    )

            # Extract arguments in the correct order for the function call
            func_args = [bound_arguments.get(arg) for arg in arg_names]
            # Add keyword-only arguments as well
            func_kwargs = {name: bound_arguments.get(name) for name in kwonly_names}

            return func(*func_args, **func_kwargs)

        return wrapper

    return decorator
