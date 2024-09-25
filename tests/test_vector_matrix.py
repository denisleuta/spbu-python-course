import pytest
import math

from vector_matrix import scalar_multyply, vector_length, angle_vectors, matrix_addition, matrix_multiply, transpose_matrix

def test_scalar_multyply():
    assert scalar_multyply([1, 2, 3], [4, 5, 6]) == 32

def test_vector_length():
    assert vector_length([3, 4]) == 5

def test_angle_vectors():
    assert pytest.approx(angle_vectors([1, 0], [0, 1])) == math.pi / 2

def test_matrix_addition():
    assert matrix_addition([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[6, 8], [10, 12]]

def test_matrix_multiply():
    assert matrix_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[19, 22], [43, 50]]

def test_transpose_matrix():
    assert transpose_matrix([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]