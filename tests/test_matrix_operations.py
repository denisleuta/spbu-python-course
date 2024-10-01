import pytest
import math

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.matrix_operations import matrix_addition, matrix_multiply, transpose_matrix


def test_matrix_addition():
    # Обычный случай
    assert matrix_addition([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[6, 8], [10, 12]]

    # Сложение с нулевой матрицей
    assert matrix_addition([[1, 2], [3, 4]], [[0, 0], [0, 0]]) == [[1, 2], [3, 4]]

    # Сложение матриц с отрицательными числами
    assert matrix_addition([[-1, -2], [-3, -4]], [[5, 6], [7, 8]]) == [[4, 4], [4, 4]]

    # Граничный случай: пустые матрицы
    assert matrix_addition([], []) == []

    # Исключение: несоответствие размеров
    try:
        matrix_addition([[1]], [[1, 2]])
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError for mismatched sizes"


def test_matrix_multiply():
    # Обычный случай
    assert matrix_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[19, 22], [43, 50]]

    # Умножение на единичную матрицу
    assert matrix_multiply([[1, 2], [3, 4]], [[1, 0], [0, 1]]) == [[1, 2], [3, 4]]

    # Умножение с нулевой матрицей
    assert matrix_multiply([[1, 2]], [[0], [0]]) == [[0]]

    # Граничный случай: пустые матрицы
    assert matrix_multiply([], []) == []

    # Исключение: несоответствие размеров
    try:
        matrix_multiply([[1]], [[1], [2]])
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError for mismatched sizes"


def test_transpose_matrix():
    # Обычный случай
    assert transpose_matrix([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]

    # Транспонирование квадратной матрицы
    assert transpose_matrix([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]

    # Транспонирование матрицы с одной строкой
    assert transpose_matrix([[1, 2]]) == [[1], [2]]

    # Транспонирование матрицы с одним столбцом
    assert transpose_matrix([[1], [2]]) == [[1, 2]]

    # Граничный случай: пустая матрица
    assert transpose_matrix([]) == []
