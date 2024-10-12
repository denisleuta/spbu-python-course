from collections import OrderedDict
from functools import wraps
from typing import Callable, Any, Dict, Tuple, Optional


def make_hashable(obj: Any) -> Any:
    """Converts a non-hashed object to a hashed one."""
    if isinstance(obj, (list, dict, set)):
        return (
            frozenset((make_hashable(k), make_hashable(v)) for k, v in obj.items())
            if isinstance(obj, dict)
            else tuple(make_hashable(i) for i in obj)
        )
    return obj


def cache_results(
    max_size: int = 0,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator for caching the results of a function based on its input arguments.

    Parameters:
    ----------
    max_size : int, optional
        The maximum number of results to cache. If set to 0 (default),
        caching is unlimited. If the cache reaches this size,
        the least recently used item will be removed to make space
        for the new result.

    Returns:
    -------
    function
        A wrapped version of the original function that caches its results.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        cache: OrderedDict[Tuple[Any, ...], Any] = OrderedDict()

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (
                tuple(make_hashable(arg) for arg in args),
                frozenset((k, make_hashable(v)) for k, v in kwargs.items()),
            )
            if key in cache:
                print(f"Cache hit for args: {args}, kwargs: {kwargs}")
                return cache[key]
            print(f"Cache miss: {args}, kwargs: {kwargs} - calculating")
            result = func(*args, **kwargs)
            if max_size > 0:
                if len(cache) >= max_size:
                    cache.popitem(last=False)
                cache[key] = result
            return result

        return wrapper

    return decorator
