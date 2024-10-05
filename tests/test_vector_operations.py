import pytest
import math

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.vector_operations import scalar_multiply, vector_length, angle_vectors


def test_scalar_multiply():
    # The normal case
    assert scalar_multiply([1, 2, 3], [4, 5, 6]) == 32

    # Scalar product with a zero vector
    assert scalar_multiply([0, 0, 0], [1, 2, 3]) == 0

    # Scalar product with negative numbers
    assert scalar_multiply([-1, -2, -3], [4, 5, 6]) == -32

    # Boundary case: empty vectors
    assert scalar_multiply([], []) == 0

    # Exception: size mismatch
    try:
        scalar_multiply([1], [1, 2])
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError for mismatched sizes"


def test_vector_length():
    # The normal case
    assert vector_length([3, 4]) == 5

    # The length of the zero vector
    assert vector_length([0, 0]) == 0

    # The length of a vector with negative numbers
    assert vector_length([-3, -4]) == 5

    # Boundary case: empty vector
    try:
        vector_length([])
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError for empty vector"


def test_angle_vectors():
    # The normal case
    assert pytest.approx(angle_vectors([1, 0], [0, 1])) == math.pi / 2

    # The angle between the opposite vectors (must be π)
    assert pytest.approx(angle_vectors([1, 0], [-1, 0])) == math.pi

    # The angle between the zero vectors (undefined)
    try:
        angle_vectors([0, 0], [1, 1])
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError for zero-length vector"

    # The angle between the vector and the zero vector (undefined)
    try:
        angle_vectors([1, 2], [0, 0])
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError for zero-length vector"
