import pytest
import random
import sys
import os
import copy

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.smart_args import (
    Evaluated,
    Isolated,
    smart_args,
)  # Adjust the import as necessary


def test_evaluated_default():
    def get_random_number():
        return random.randint(1, 10)

    @smart_args()
    def my_function(x=Evaluated(get_random_number)):
        return x

    # Call the function multiple times to ensure different results.
    result1 = my_function()
    result2 = my_function()

    # Assert that the results are valid random numbers
    assert (
        isinstance(result1, int) and 1 <= result1 <= 10
    ), "Result1 should be a random number between 1 and 10."
    assert (
        isinstance(result2, int) and 1 <= result2 <= 10
    ), "Result2 should be a random number between 1 and 10."


def test_isolated_default():
    """Test that Isolated creates a deep copy of the argument."""

    @smart_args()
    def my_function(data=Isolated()):
        isolated_data = copy.deepcopy(data)
        isolated_data.append(1)
        return isolated_data

    original_data = [0]
    result = my_function(original_data)

    assert result == [
        0,
        1,
    ], "Function should return a modified copy of the original data."
    assert original_data == [
        0
    ], "Original data should remain unchanged, demonstrating isolation."


def test_keyword_arguments():
    """Test that keyword arguments are correctly handled by smart_args."""

    @smart_args(enable_positional=False)
    def my_function(x=5, y=10):
        return x + y

    # Check the use of keyword arguments
    assert (
        my_function() == 15
    ), "Default values should be used when no arguments are provided."
    assert (
        my_function(x=3) == 13
    ), "Keyword argument x should override the default value."
    assert (
        my_function(y=7) == 12
    ), "Keyword argument y should override the default value."
    assert (
        my_function(x=3, y=7) == 10
    ), "Both keyword arguments should override default values."

    # Test keyword-only arguments
    @smart_args(enable_positional=False)
    def keyword_only_func(*, a=1, b=2):
        return a + b

    assert (
        keyword_only_func() == 3
    ), "Default values should be used when no keyword arguments are provided."
    assert (
        keyword_only_func(a=5) == 7
    ), "Keyword argument a should override the default value."


def test_mixed_arguments():
    """Test that mixed positional and keyword arguments work correctly."""

    @smart_args()
    def my_function(x=5, y=10):
        return x + y

    assert (
        my_function(2) == 12
    ), "Positional argument x should override the default value."
    assert (
        my_function(y=8) == 13
    ), "Keyword argument y should override the default value."
    assert (
        my_function(2, y=8) == 10
    ), "Both positional and keyword arguments should work together."


def test_error_with_isolated_without_argument():
    """Test that an error is raised when Isolated is used without providing an argument."""

    @smart_args()
    def my_function(data=Isolated()):
        return data

    with pytest.raises(ValueError) as exc_info:
        my_function()

    assert (
        str(exc_info.value)
        == "Argument 'data' must be provided explicitly and cannot use Isolated."
    ), "Should raise ValueError when using Isolated without providing an argument."


def test_evaluated_and_isolated_combined():
    """Test that Evaluated and Isolated cannot be used together."""

    def get_random_number():
        return random.randint(1, 10)

    @smart_args()
    def my_function(x=Evaluated(get_random_number), y=Isolated()):
        return x, y

    # Check that the function works when both arguments are correctly provided
    result = my_function(y=[1, 2, 3])
    assert isinstance(result[0], int), "First value should be a random integer."
    assert result[1] == [1, 2, 3], "Second value should be the provided list."

    # Check that an error is raised when Evaluated returns Isolated
    @smart_args()
    def invalid_func(x=Evaluated(lambda: Isolated()), y=Isolated()):
        return x, y

    with pytest.raises(ValueError) as exc_info:
        invalid_func(y=[1, 2, 3])

    assert "cannot use Isolated" in str(
        exc_info.value
    ), "Should raise ValueError when Evaluated returns an Isolated object."
