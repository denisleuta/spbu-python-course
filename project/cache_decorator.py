from collections import OrderedDict
from functools import wraps


def cache_results(max_size=0):
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
