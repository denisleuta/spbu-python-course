import math
from typing import List


def scalar_multiply(v1: List[float], v2: List[float]) -> float:
    """
    Вычисляет скалярное произведение двух векторов.

    Параметры:
    v1 (List[float]): Первый вектор.
    v2 (List[float]): Второй вектор.

    Возвращает:
    float: Скалярное произведение двух векторов.

    Исключения:
    ValueError: Если размеры векторов не совпадают.
    """
    if len(v1) != len(v2):
        raise ValueError("Размеры векторов должны совпадать.")

    return sum(x * y for x, y in zip(v1, v2))


def vector_length(v: List[float]) -> float:
    """
    Вычисляет длину (норму) вектора.

    Параметры:
    v (List[float]): Вектор.

    Возвращает:
    float: Длина вектора.

    Исключения:
    ValueError: Если вектор пустой.
    """
    if not v:
        raise ValueError("Вектор не должен быть пустым.")

    return math.sqrt(scalar_multiply(v, v))


def angle_vectors(v1: List[float], v2: List[float]) -> float:
    """
    Вычисляет угол между двумя векторами в радианах.

    Параметры:
    v1 (List[float]): Первый вектор.
    v2 (List[float]): Второй вектор.

    Возвращает:
    float: Угол между двумя векторами в радианах.

    Исключения:
    ValueError: Если длина одного из векторов равна нулю.
    """
    length_v1 = vector_length(v1)
    length_v2 = vector_length(v2)

    if length_v1 == 0 or length_v2 == 0:
        raise ValueError(
            "Длина одного из векторов равна нулю, угол не может быть определен."
        )

    return math.acos(scalar_multiply(v1, v2) / (length_v1 * length_v2))
