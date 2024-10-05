import pytest
import random
import sys
import os
import copy

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.smart_args import smart_args, Isolated, Evaluated


def get_random_number():
    return 42  # For testing with a fixed value


@smart_args
def check_isolation(*, d=Isolated()):
    d = d.copy()
    d["a"] = 0
    return d


@smart_args
def check_evaluation(*, x=get_random_number(), y=Evaluated(get_random_number)):
    return x, y


def test_check_isolation():
    no_mutable = {"a": 10}
    result = check_isolation(d=no_mutable)

    assert result == {"a": 0}
    assert no_mutable == {"a": 10}


def test_check_evaluation():
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
    with pytest.raises(ValueError) as excinfo:
        check_isolation()  # Should raise an error due to Isolated

    assert "must be provided" in str(excinfo.value)
