import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.cache import cache_results


@cache_results(max_size=3)
def add(a, b):
    return a + b


@cache_results(max_size=3)
def count_elements(collection):
    return len(collection)


def test_cache_hit_miss(capfd):
    assert add(1, 2) == 3
    captured = capfd.readouterr()
    assert "Cache miss" in captured.out

    assert add(1, 2) == 3
    captured = capfd.readouterr()
    assert "Cache hit" in captured.out

    assert add(2, 3) == 5
    captured = capfd.readouterr()
    assert "Cache miss" in captured.out


def test_cache_builtin_function():
    # Test cache with Python built-in function (sum)
    @cache_results(max_size=2)
    def built_in_sum(values):
        return sum(values)

    assert built_in_sum([1, 2, 3]) == 6  # Cache miss
    assert built_in_sum([1, 2, 3]) == 6  # Cache hit
    assert built_in_sum([4, 5]) == 9  # Cache miss


def test_cache_non_hashable_arguments():
    # Test cache with non-hashable argument (list)
    @cache_results(max_size=2)
    def list_sum(collection):
        return sum(collection)

    assert list_sum([1, 2, 3]) == 6  # Cache miss
    assert list_sum([1, 2, 3]) == 6  # Cache hit


def test_cache_iteration_tracking():
    iterations = []

    @cache_results(max_size=3)
    def track_iterations(a, b):
        result = a + b
        iterations.append((a, b))
        return result

    track_iterations(1, 2)  # 1st call
    track_iterations(2, 3)  # 2nd call
    track_iterations(3, 4)  # 3rd call
    track_iterations(4, 5)  # Cache limit reached, 1st call evicted

    assert len(iterations) == 4  # Ensure each call is tracked
