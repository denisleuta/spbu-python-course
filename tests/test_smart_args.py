import pytest
import random
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.smart_args import (
    Evaluated,
    Isolated,
    smart_args,
)  # Adjust the import as necessary


def test_evaluated_default():
    """Test that Evaluated correctly evaluates a function when called."""

    def get_random_number():
        return random.randint(1, 10)

    @smart_args()
    def my_function(x=Evaluated(get_random_number)):
        return x

    result = my_function()
    assert (
        isinstance(result, int) and 1 <= result <= 10
    ), "Result should be a random number between 1 and 10."


def test_isolated_default():
    """Test that Isolated creates a deep copy of the argument."""

    @smart_args()
    def my_function(data=Isolated()):
        # Create a mutable list to demonstrate isolation.
        data_list = []
        data_list.append(1)
        return data_list

    original_data = []
    result = my_function(original_data)
    assert result == [1], "Function should return a modified copy of the original data."
    assert original_data == [], "Original data should remain unchanged."


def test_positional_arguments():
    """Test that positional arguments are correctly handled by smart_args."""

    @smart_args(enable_positional=True)
    def my_function(x=5, y=10):
        return x + y

    assert (
        my_function() == 15
    ), "Default values should be used when no arguments are provided."
    assert (
        my_function(3) == 13
    ), "Positional argument x should override the default value."
    assert (
        my_function(3, 7) == 10
    ), "Both positional arguments should override default values."


def test_keyword_arguments():
    """Test that keyword arguments are correctly handled by smart_args."""

    @smart_args(enable_positional=False)
    def my_function(x=5, y=10):
        return x + y

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
        == "Argument 'data' must be provided and cannot use Isolated."
    ), "Should raise ValueError when using Isolated without providing an argument."


if __name__ == "__main__":
    pytest.main()
