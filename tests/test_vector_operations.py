import pytest
import math

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.vector_operations import scalar_multiply, vector_length, angle_vectors


def test_scalar_multiply():
    # Обычный случай
    assert scalar_multiply([1, 2, 3], [4, 5, 6]) == 32

    # Скалярное произведение с нулевым вектором
    assert scalar_multiply([0, 0, 0], [1, 2, 3]) == 0

    # Скалярное произведение с отрицательными числами
    assert scalar_multiply([-1, -2, -3], [4, 5, 6]) == -32

    # Граничный случай: пустые векторы
    assert scalar_multiply([], []) == 0

    # Исключение: несоответствие размеров
    try:
        scalar_multiply([1], [1, 2])
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError for mismatched sizes"


def test_vector_length():
    # Обычный случай
    assert vector_length([3, 4]) == 5

    # Длина нулевого вектора
    assert vector_length([0, 0]) == 0

    # Длина вектора с отрицательными числами
    assert vector_length([-3, -4]) == 5

    # Граничный случай: пустой вектор
    try:
        vector_length([])
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError for empty vector"


def test_angle_vectors():
    # Обычный случай
    assert pytest.approx(angle_vectors([1, 0], [0, 1])) == math.pi / 2

    # Угол между одинаковыми векторами (должен быть 0)
    assert pytest.approx(angle_vectors([1, 2], [1, 2])) == 0

    # Угол между противоположными векторами (должен быть π)
    assert pytest.approx(angle_vectors([1, 0], [-1, 0])) == math.pi

    # Угол между нулевыми векторами (неопределен)
    try:
        angle_vectors([0, 0], [1, 1])
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError for zero-length vector"

    # Угол между вектором и нулевым вектором (неопределен)
    try:
        angle_vectors([1, 2], [0, 0])
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError for zero-length vector"
