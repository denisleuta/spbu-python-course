import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.cache import cache_results


@cache_results(2)
def add(x, y):
    """
    Add two numbers together.

    This function takes two numerical inputs and returns their sum.
    The results of this function are cached to improve performance
    for frequently called inputs, with a maximum cache size defined
    by the decorator.

    Parameters:
    ----------
    x : int or float
        The first number to be added.
    y : int or float
        The second number to be added.

    Returns:
    -------
    int or float
        The sum of `x` and `y`.
    """
    return x + y


def test_cache():
    """
    Test the caching functionality of the `add` function.

    This test verifies that the `add` function correctly caches
    results based on its input arguments, ensuring that repeated
    calls with the same arguments return the cached result
    instead of recalculating. The maximum cache size is set to
    2, meaning that once the cache reaches this size,
    the least recently used item will be removed.

    The test checks the following scenarios:
    - The first call to `add(1, 2)` calculates and caches the result.
    - The second call to `add(1, 2)` retrieves the result from the cache.
    - Calls to `add(3, 4)` and `add(5, 6)` calculate and cache their results.
    - The cache is expected to contain results for the last two unique calls.
    - Finally, when `add(1, 2)` is called again after the cache has been cleared,
      it should recalculate the result instead of retrieving it from the cache.

    Example:
    --------
    The sequence of assertions in this test checks that:
    - `add(1, 2)` results in `3`
    - Repeated calls to `add(1, 2)` use the cache and still return `3`
    - New unique calls like `add(3, 4)` and `add(5, 6)` return `7` and `11`, respectively.
    - After the cache is cleared, calling `add(1, 2)` again should recalculate `3`.
    """
    assert add(1, 2) == 3
    assert add(1, 2) == 3  # From the cache
    assert add(3, 4) == 7
    assert add(5, 6) == 11
    assert add(1, 2) == 3  # This is not from cache; cache has been cleared
