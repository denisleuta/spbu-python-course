import pytest
import itertools
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.rgba_decorator import get_rgba_element, get_prime, prime_generator


# Test for valid RGBA element generation with optimized method
def test_rgba_element_optimized():
    """
    Tests if the optimized RGBA generator returns the expected RGBA vector
    for a given index without generating all combinations.
    """
    rgba_index = 100
    elem = get_rgba_element(rgba_index)
    assert elem == (0, 0, 1, 98), f"Expected element (0, 0, 1, 98), but got {elem}"


# Test for invalid RGBA index (out of range)
def test_rgba_element_out_of_range():
    """
    Tests if the function raises an IndexError for an out-of-range RGBA index.
    """
    total_combinations = 256 * 256 * 256 * 51
    with pytest.raises(IndexError):
        get_rgba_element(total_combinations)


# Test for negative RGBA index
def test_rgba_element_negative_index():
    """
    Tests if the function raises an IndexError for a negative RGBA index.
    """
    with pytest.raises(IndexError):
        get_rgba_element(-1)


# Parametrized test for prime numbers with optimized generator
@pytest.mark.parametrize(
    "k, expected",
    [
        (1, 2),  # First prime
        (2, 3),  # Second prime
        (3, 5),  # Third prime
        (10, 29),  # 10th prime
        (100, 541),  # 100th prime
        (1000, 7919),  # 1000th prime
    ],
)
def test_prime_numbers_optimized(k: int, expected: int):
    """
    Parametrized test to verify if the k-th prime number is correctly returned
    using the optimized prime number generator.
    """
    primes = prime_generator(limit=1000)
    assert (
        next(itertools.islice(primes, k - 1, k)) == expected
    ), f"Expected prime {expected}, but got a different result"


# Test for invalid prime number index (negative)
def test_prime_negative_index():
    """
    Tests if the prime number generator raises an IndexError for a negative index.
    """
    with pytest.raises(ValueError):
        get_prime(-5)  # Negative index should raise an error


def test_prime_non_integer():
    """
    Tests if the prime number generator raises a TypeError for a non-integer index.
    """
    with pytest.raises(TypeError):
        get_prime(2.5)  # Non-integer index should raise a TypeError


# Additional edge case tests
def test_rgba_element_edge_cases():
    # Test for the first and last valid index
    assert get_rgba_element(0) == (0, 0, 0, 0), "Expected RGBA vector (0, 0, 0, 0)"
    total_combinations = 256 * 256 * 256 * 51 - 1
    assert get_rgba_element(total_combinations) == (
        255,
        255,
        255,
        100,
    ), "Expected RGBA vector (255, 255, 255, 100)"


def test_prime_zero_index():
    with pytest.raises(ValueError):
        get_prime(0)  # Should raise a ValueError
