import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.cache import cache_results


@cache_results(2)
def add(x, y):
    return x + y


def test_cache():
    assert add(1, 2) == 3
    assert add(1, 2) == 3  # From the cashe
    assert add(3, 4) == 7
    assert add(5, 6) == 11
    assert add(1, 2) == 3  # This is not a cache, because the cache is cleared
