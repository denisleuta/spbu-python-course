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

    Example:
    --------
    def get_random_number():
        return random.randint(1, 10)

    @smart_args
    def my_function(x=Evaluated(get_random_number)):
        return x

    result = my_function()  # result will be a random number
    """

    def __init__(self, func):
        self.func = func

    def __call__(self):
        return self.func()


class Isolated:
    """
    A marker class used to indicate that a function argument should be
    treated as isolated.

    When used as a default value for a function parameter, it indicates
    that the argument should not be modified or shared outside the function.
    Instead, a deep copy of the argument will be created to ensure
    isolation.

    Example:
    --------
    @smart_args
    def my_function(data=Isolated()):
        # 'data' will be isolated, and changes will not affect the original.
    """

    pass


def smart_args(func):
    """
    A decorator that enhances a function's parameter handling.

    This decorator allows for dynamic evaluation and isolation of function
    arguments. It processes default values based on their types:
    - If the default value is an instance of `Evaluated`, it will be called
      to generate the value when the function is invoked.
    - If the default value is an instance of `Isolated`, a deep copy of the
      provided argument will be made to ensure the original value remains unchanged.
    - If the default value is a mutable type (like a dictionary), a deep
      copy will also be created.

    Parameters:
    ----------
    func : callable
        The function to be decorated.

    Returns:
    -------
    callable
        A wrapped version of the input function with enhanced parameter
        handling.

    Raises:
    ------
    ValueError
        If an `Isolated` parameter is used without an accompanying value.

    Example:
    --------
    @smart_args
    def my_function(a=Isolated(), b=Evaluated(lambda: 42)):
        return a, b()

    my_function(10)  # Returns (10, 42)
    """

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
                # Create a deep copy of the provided argument
                if name in kwargs:
                    bound_arguments.arguments[name] = copy.deepcopy(kwargs[name])
                else:
                    raise ValueError(
                        f"Argument '{name}' must be provided and cannot use Isolated."
                    )
            elif isinstance(default, dict):  # Example for mutable types
                bound_arguments.arguments[name] = copy.deepcopy(default)

        return func(*bound_arguments.args, **bound_arguments.kwargs)

    return wrapper
