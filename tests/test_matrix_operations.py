import pytest

import math

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.matrix_operations import matrix_addition, matrix_multiply, transpose_matrix


def test_matrix_addition():
    # The normal case
    assert matrix_addition([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[6, 8], [10, 12]]

    # Addition with a zero matrix
    assert matrix_addition([[1, 2], [3, 4]], [[0, 0], [0, 0]]) == [[1, 2], [3, 4]]

    # Addition with negative nums
    assert matrix_addition([[-1, -2], [-3, -4]], [[5, 6], [7, 8]]) == [[4, 4], [4, 4]]

    # Boundary case: empty matrices
    assert matrix_addition([], []) == []

    # Exception: size mismatch
    try:
        matrix_addition([[1]], [[1, 2]])
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError for mismatched sizes"


def test_matrix_multiply():
    # The normal case (square matrices)
    assert matrix_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[19, 22], [43, 50]]

    # Multiplication by a single matrix (identity)
    assert matrix_multiply([[1, 2], [3, 4]], [[1, 0], [0, 1]]) == [[1, 2], [3, 4]]

    # Multiplication with a zero matrix
    assert matrix_multiply([[1, 2]], [[0], [0]]) == [[0]]

    # Test with non-square matrices (2x3 and 3x2)
    assert matrix_multiply([[1, 2, 3], [4, 5, 6]], [[7, 8], [9, 10], [11, 12]]) == [
        [58, 64],
        [139, 154],
    ]

    # Test with non-square matrices (3x2 and 2x3)
    assert matrix_multiply([[1, 2], [3, 4], [5, 6]], [[7, 8], [9, 10]]) == [
        [25, 28],
        [57, 64],
        [89, 100],
    ]

    # Boundary case: empty matrices
    assert matrix_multiply([], []) == []

    # Exception: size mismatch
    try:
        matrix_multiply([[1]], [[1], [2]])
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError for mismatched sizes"


def test_transpose_matrix():
    # The normal case
    assert transpose_matrix([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]

    # Transposing a square matrix
    assert transpose_matrix([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]

    # Transposing a matrix with a single row
    assert transpose_matrix([[1, 2]]) == [[1], [2]]

    # Transposing a matrix with one column
    assert transpose_matrix([[1], [2]]) == [[1, 2]]

    # Boundary case: an empty matrix
    assert transpose_matrix([]) == []
