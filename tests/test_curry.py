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
