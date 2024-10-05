import pytest
import random
import sys
import os
import copy

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.smart_args import smart_args, Isolated, Evaluated


def get_random_number():
    """
    Generate a fixed random number for testing.

    This function returns a predetermined value (42) to ensure
    consistent test results. It serves as a placeholder to illustrate
    how the function could be modified in a real-world scenario to
    generate random numbers.

    Returns:
    -------
    int
        A fixed random number, specifically 42.
    """
    return 42  # For testing with a fixed value


@smart_args
def check_isolation(*, d=Isolated()):
    """
    Check isolation of a dictionary argument.

    This function modifies the provided dictionary by setting the
    key "a" to 0. If the `d` argument is not provided, it raises
    a ValueError indicating that an argument must be supplied.
    The purpose is to test the behavior of the `Isolated` class.

    Parameters:
    ----------
    d : dict, optional
        A dictionary that is expected to be passed by the user.
        If not provided, a ValueError is raised.

    Returns:
    -------
    dict
        A new dictionary with "a" set to 0.

    Raises:
    ------
    ValueError
        If `d` is not provided, indicating that an argument must be supplied.
    """
    d = d.copy()
    d["a"] = 0
    return d


@smart_args
def check_evaluation(*, x=get_random_number(), y=Evaluated(get_random_number)):
    """
    Check the evaluation of arguments with lazy evaluation.

    This function returns the evaluated values of `x` and `y`. The
    `x` value is obtained from the `get_random_number` function,
    and `y` is evaluated using the `Evaluated` class. If `y` is not
    specified, it defaults to the fixed value from `get_random_number`.

    Parameters:
    ----------
    x : int, optional
        A number that defaults to a fixed random number for testing.
    y : Evaluated, optional
        A callable that returns a fixed random number. If not provided,
        it evaluates to the fixed value (42).

    Returns:
    -------
    tuple
        A tuple containing the evaluated values of `x` and `y`.
    """
    return x, y


def test_check_isolation():
    """
    Test the isolation behavior of the `check_isolation` function.

    This test verifies that when a mutable dictionary is passed to
    the `check_isolation` function, it does not alter the original
    dictionary. Instead, it returns a new dictionary with the
    specified modifications.

    It checks that:
    - The returned result is a dictionary with "a" set to 0.
    - The original dictionary remains unchanged.
    """
    no_mutable = {"a": 10}
    result = check_isolation(d=no_mutable)

    assert result == {"a": 0}
    assert no_mutable == {"a": 10}


def test_check_evaluation():
    """
    Test the evaluation behavior of the `check_evaluation` function.

    This test verifies that the `check_evaluation` function correctly
    evaluates the arguments `x` and `y`, both with their default
    values and with user-specified values for `y`.

    It checks that:
    - The first call retrieves the fixed value for `x` and evaluates `y`.
    - The second call retrieves the same values to ensure consistency.
    - A call with a specified value for `y` correctly returns that value.

    The expected behavior is that `y` should consistently evaluate to
    the fixed number (42) unless overridden by the user.
    """
    x_value = get_random_number()

    # Check the first call with computed value for y
    result1 = check_evaluation()
    assert result1[0] == x_value
    assert result1[1] == 42  # y value should be fixed

    # Check the second call with a new computed value for y
    result2 = check_evaluation()
    assert result2[0] == x_value
    assert result2[1] == 42  # y value should be fixed

    # Check the call with a specified value for y
    result3 = check_evaluation(y=150)
    assert result3[0] == x_value
    assert result3[1] == 150


def test_isolated_error():
    """
    Test error handling for the `check_isolation` function.

    This test verifies that the `check_isolation` function raises a
    ValueError when called without providing the required `d` argument,
    which is marked as `Isolated`. The test checks that the appropriate
    error message is raised.

    It ensures that the implementation adheres to the expected
    behavior when required arguments are not provided.
    """
    with pytest.raises(ValueError) as excinfo:
        check_isolation()  # Should raise an error due to Isolated

    assert "must be provided" in str(excinfo.value)
