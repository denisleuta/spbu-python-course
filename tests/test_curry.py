import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.curry import curry_explicit, uncurry_explicit


def test_curry_basic():
    f = curry_explicit(lambda x, y: x + y, 2)
    assert f(3)(4) == 7


def test_uncurry_basic():
    f = curry_explicit(lambda x, y: x + y, 2)
    g = uncurry_explicit(f, 2)
    assert g(3, 4) == 7


def test_invalid_arity():
    with pytest.raises(TypeError):
        f = curry_explicit(lambda x, y: x + y, 2)
        f(3)(4)(5)


def test_negative_arity():
    with pytest.raises(ValueError):
        curry_explicit(lambda x, y: x + y, -1)


def test_curry_zero_arity():
    f = curry_explicit(lambda: 42, 0)
    assert f() == 42


def test_uncurry_zero_arity():
    f = curry_explicit(lambda: 42, 0)
    g = uncurry_explicit(f, 0)
    assert g() == 42
