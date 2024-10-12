import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.curry import curry_explicit, uncurry_explicit


def test_curry_basic():
    """
    Test the basic functionality of the `curry_explicit` function.

    This test verifies that a curried function can be called
    with its arguments in a stepwise manner and produces the correct result.

    Example:
    --------
    Calling the curried function with (3)(4) should return 7.
    """
    f = curry_explicit(lambda x, y: x + y, 2)
    assert f(3)(4) == 7


def test_uncurry_basic():
    """
    Test the basic functionality of the `uncurry_explicit` function.

    This test ensures that a curried function can be converted back
    to a standard function that accepts all arguments at once and
    produces the correct result.

    Example:
    --------
    Calling the uncurried function with (3, 4) should return 7.
    """
    f = curry_explicit(lambda x, y: x + y, 2)
    g = uncurry_explicit(f, 2)
    assert g(3, 4) == 7


def test_invalid_arity():
    """
    Test that calling a curried function with too many arguments raises a TypeError.

    This test checks that if a curried function is called with
    more arguments than it expects, a TypeError is raised.
    """
    with pytest.raises(TypeError):
        f = curry_explicit(lambda x, y: x + y, 2)
        f(3)(4)(5)


def test_negative_arity():
    """
    Test that providing a negative arity raises a ValueError.

    This test verifies that the `curry_explicit` function raises a
    ValueError when a negative arity is given, as negative arity
    is invalid.
    """
    with pytest.raises(ValueError):
        curry_explicit(lambda x, y: x + y, -1)


def test_curry_zero_arity():
    """
    Test the functionality of the `curry_explicit` function with zero arity.

    This test ensures that a function with zero arity can be
    correctly called without any arguments and returns the expected result.

    Example:
    --------
    Calling the curried function with no arguments should return 42.
    """
    f = curry_explicit(lambda: 42, 0)
    assert f() == 42


def test_uncurry_zero_arity():
    """
    Test the functionality of the `uncurry_explicit` function with zero arity.

    This test ensures that a curried function with zero arity can
    be correctly converted back to a standard function that
    accepts no arguments and returns the expected result.

    Example:
    --------
    Calling the uncurried function with no arguments should return 42.
    """
    f = curry_explicit(lambda: 42, 0)
    g = uncurry_explicit(f, 0)
    assert g() == 42


def test_curry_and_uncurry_built_in_functions():
    """
    Test currying and uncurrying of built-in functions.
    """

    # Test the sum function with arity 2
    curried_sum = curry_explicit(sum, 2)
    assert curried_sum(1)(2) == 3  # Check partial application
    assert curried_sum(1, 2) == 3  # Check multiple argument application

    # Test the max function with arity 2
    curried_max = curry_explicit(max, 2)
    assert curried_max(1)(2) == 2  # Check partial application
    assert curried_max(1, 2) == 2  # Check multiple argument application

    # Test the min function with arity 2
    curried_min = curry_explicit(min, 2)
    assert curried_min(1)(2) == 1  # Check partial application
    assert curried_min(1, 2) == 1  # Check multiple argument application

    # Check uncurry for the sum function
    uncurried_sum = uncurry_explicit(curried_sum, 2)
    assert uncurried_sum(1, 2) == 3

    # Check uncurry for the max function
    uncurried_max = uncurry_explicit(curried_max, 2)
    assert uncurried_max(1, 2) == 2

    # Check uncurry for the min function
    uncurried_min = uncurry_explicit(curried_min, 2)
    assert uncurried_min(1, 2) == 1


def test_exceptions():
    """
    Test exception handling for curry and uncurry functions.
    """

    # Test that ValueError is raised for negative arity
    with pytest.raises(ValueError):
        curry_explicit(sum, -1)

    # Test that TypeError is raised when more arguments are passed than expected
    curried_sum = curry_explicit(sum, 2)  # Define curried_sum again for scope
    with pytest.raises(TypeError):
        curried_sum(1, 2, 3)  # Passing more arguments than expected

    # Test that ValueError is raised for negative arity in uncurry
    with pytest.raises(ValueError):
        uncurry_explicit(curried_sum, -1)

    # Test that TypeError is raised when not enough arguments are passed to uncurried function
    uncurried_sum = uncurry_explicit(curried_sum, 2)  # Define uncurried_sum for scope
    with pytest.raises(TypeError):
        uncurried_sum(1)  # Passing insufficient arguments
