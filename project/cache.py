from collections import OrderedDict
from functools import wraps


def cache_results(max_size=0):
    """
    Decorator for caching the results of a function based on its input arguments.

    This decorator allows you to cache the return values of a function,
    so that if the same inputs are provided again, the cached value is returned
    instead of executing the function again. This can improve performance
    for functions with expensive computations.

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

    Example:
    --------
    @cache_results(max_size=5)
    def expensive_computation(x, y):
        # Some time-consuming calculations
        return x + y

    The first call to `expensive_computation(1, 2)` will execute the function,
    and subsequent calls with the same arguments will return the cached result.
    If the cache exceeds the specified `max_size`, the oldest cached
    result will be discarded.

    """

    def decorator(func):
        cache = OrderedDict()

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            if key in cache:
                return cache[key]
            result = func(*args, **kwargs)
            if max_size > 0:
                if len(cache) >= max_size:
                    cache.popitem(last=False)
                cache[key] = result
            return result

        return wrapper

    return decorator
