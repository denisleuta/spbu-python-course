import pytest
import math

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.matrix_operations import matrix_addition, matrix_multiply, transpose_matrix

def test_matrix_additions():
    assert matrix_addition([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[6, 8], [10, 12]]

def test_matrix_multiply():
    assert matrix_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[19, 22], [43, 50]]

def test_transpose_matrix():
    assert transpose_matrix([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    