import pytest
import random
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.smart_args import smart_args, Isolated, Evaluated


@smart_args
def check_isolation(*, d=Isolated()):
    d["a"] = 0
    return d


@smart_args
def check_evaluation(*, x=Evaluated(lambda: random.randint(0, 100))):
    return x


def test_isolated():
    no_mutable = {"a": 10}
    result = check_isolation(d=no_mutable)
    assert result == {"a": 0}
    assert no_mutable == {"a": 10}  # Original object dom't change


def test_evaluated(monkeypatch):
    monkeypatch.setattr(
        random, "randint", lambda a, b: 42
    )  # Substituting a random number for determinism
    assert check_evaluation() == 42
    assert check_evaluation() == 42  # A repeat call will return 42 again
