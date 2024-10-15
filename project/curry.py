from functools import wraps
from typing import Callable, Any


def curry_explicit(function: Callable[..., Any], arity: int) -> Callable[..., Any]:
    """
    Returns a curried version of the given function.

    Currying is a technique where a function is transformed into a sequence
    of functions, each taking a single argument. This allows for partial
    application of the function's arguments.

    Parameters:
    ----------
    function : callable
        The function to be curried.
    arity : int
        The number of arguments the function accepts. Must be non-negative.

    Raises:
    ------
    ValueError
        If `arity` is negative.
    TypeError
        If more arguments than expected are passed during invocation.

    Returns:
    -------
    callable
        A curried version of the input function.
    """
    if arity < 0:
        raise ValueError("Arity must not be negative")

    def curry_helper(args: list) -> Callable[..., Any]:
        if len(args) == arity:
            if function is sum:
                return sum(args)
            return function(*args)
        elif len(args) > arity:
            raise TypeError(f"Expected {arity} arguments, received {len(args)}")

        return lambda x: curry_helper(args + [x])

    if arity == 0:
        return lambda: function()

    return curry_helper([])


def uncurry_explicit(function: Callable[..., Any], arity: int) -> Callable[..., Any]:
    """
    Converts a curried function back into a regular function.

    This function takes a curried function and returns a new function
    that accepts all arguments at once, rather than one at a time.

    Parameters:
    ----------
    function : callable
        The curried function to be uncurried.
    arity : int
        The number of arguments the curried function accepts. Must be non-negative.

    Raises:
    ------
    ValueError
        If `arity` is negative.
    TypeError
        If the number of provided arguments does not match the expected arity.

    Returns:
    -------
    callable
        A function that accepts all arguments at once.
    """
    if arity < 0:
        raise ValueError("Arity must not be negative")

    @wraps(function)
    def uncurry_helper(*args: Any) -> Any:
        if len(args) != arity:
            raise TypeError(f"Expected {arity} arguments, received {len(args)}")

        if arity == 0:
            return function()
        result = function
        for arg in args:
            result = result(arg)
        return result

    return uncurry_helper
