import pytest
import sys
import os
from typing import Tuple

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.rgba_decorator import (
    get_rgba_element,
    get_prime,
    TOTAL_COMBINATIONS,
)

# Tests for RGBA functionality
def test_rgba_element_optimized() -> None:
    """
    Tests the optimized RGBA element retrieval function.

    Checks that when passing index 100, the function returns
    the expected value (0, 0, 1, 98).
    """
    rgba_index = 100
    elem = get_rgba_element(rgba_index)
    assert elem == (0, 0, 1, 98), f"Expected element (0, 0, 1, 98), but got {elem}"


def test_rgba_element_out_of_range() -> None:
    """
    Tests that the function raises an IndexError when the RGBA index
    is out of the valid range.
    """
    with pytest.raises(IndexError):
        get_rgba_element(TOTAL_COMBINATIONS)


def test_rgba_element_negative_index() -> None:
    """
    Tests that the function raises an IndexError for a negative RGBA index.
    """
    with pytest.raises(IndexError):
        get_rgba_element(-1)


@pytest.mark.parametrize(
    "index, expected",
    [
        (0, (0, 0, 0, 0)),
        (1, (0, 0, 0, 2)),
        (TOTAL_COMBINATIONS - 1, (255, 255, 255, 100)),
    ],
)
def test_rgba_element_various_cases(
    index: int, expected: Tuple[int, int, int, int]
) -> None:
    """
    Parameterized test to check various RGBA indices and their
    corresponding values.

    Args:
        index (int): The RGBA element index.
        expected (Tuple[int, int, int, int]): The expected RGBA element value.
    """
    assert get_rgba_element(index) == expected


# Tests for prime number functionality
@pytest.mark.parametrize(
    "k, expected", [(1, 2), (2, 3), (3, 5), (5, 11), (10, 29), (15, 47), (100, 541)]
)
def test_prime_decorator_sequential_calls(k: int, expected: int) -> None:
    """
    Parameterized test to verify the correctness of returned prime numbers
    through multiple sequential calls to the prime-decorated function.

    This test ensures that the function correctly returns the k-th prime
    number on multiple invocations without restarting the generator.

    Args:
        k (int): The index of the prime number.
        expected (int): The expected prime number.
    """
    assert (
        get_prime(k) == expected
    ), f"Expected prime {expected} at position {k}, but got a different result"


def test_prime_multiple_calls() -> None:
    """
    Tests that multiple calls to get_prime() with increasing k do not restart
    the generator, and each call returns the correct prime number in sequence.
    """
    primes = [get_prime(1), get_prime(2), get_prime(3), get_prime(4), get_prime(5)]
    assert primes == [
        2,
        3,
        5,
        7,
        11,
    ], f"Expected primes [2, 3, 5, 7, 11], but got {primes}"


def test_prime_negative_index() -> None:
    """
    Tests that the function raises a ValueError for a negative index
    for the prime number.
    """
    with pytest.raises(ValueError):
        get_prime(-5)


def test_prime_non_integer() -> None:
    """
    Tests that the function raises a TypeError for a non-integer index
    for the prime number.
    """
    with pytest.raises(TypeError):
        get_prime(2.5)


def test_prime_zero_index() -> None:
    """
    Tests that the function raises a ValueError for a zero index
    for the prime number.
    """
    with pytest.raises(ValueError):
        get_prime(0)
