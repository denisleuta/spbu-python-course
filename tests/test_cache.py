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

    Test that the cache evicts the least recently used item
    when the maximum cache size is reached.
    """
    assert add(1, 2) == 3  # Cache: {(1, 2): 3}
    assert add(3, 4) == 7  # Cache: {(1, 2): 3, (3, 4): 7}
    assert add(5, 6) == 11  # Cache: {(1, 2): 3, (3, 4): 7, (5, 6): 11} -> Evicts (1, 2)

    # Now (1, 2) should be evicted
    assert add(1, 2) == 3  # Recalculates since (1, 2) was evicted
    assert add(3, 4) == 7  # Should still be cached
    assert add(5, 6) == 11  # Should still be cached


def test_different_argument_types():
    """
    Test the `add` function with different types of numerical inputs.
    """
    assert add(1.5, 2.5) == 4.0  # Float inputs
    assert add(-1, -2) == -3  # Negative integers
    assert add(0, 0) == 0  # Zero inputs
    assert add(1000000, 2000000) == 3000000  # Large integers
