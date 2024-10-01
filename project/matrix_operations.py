from typing import List


def matrix_addition(m1: List[List[float]], m2: List[List[float]]) -> List[List[float]]:
    """
    Складывает две матрицы.

    Параметры:
    m1 (List[List[float]]): Первая матрица.
    m2 (List[List[float]]): Вторая матрица.

    Возвращает:
    List[List[float]]: Результат сложения двух матриц.

    Исключения:
    ValueError: Если размеры матриц не совпадают.
    """
    if len(m1) != len(m2) or any(len(row1) != len(row2) for row1, row2 in zip(m1, m2)):
        raise ValueError("Размеры матриц должны совпадать.")

    return [[x + y for x, y in zip(row1, row2)] for row1, row2 in zip(m1, m2)]


def matrix_multiply(m1: List[List[float]], m2: List[List[float]]) -> List[List[float]]:
    """
    Умножает две матрицы.

    Параметры:
    m1 (List[List[float]]): Первая матрица.
    m2 (List[List[float]]): Вторая матрица.

    Возвращает:
    List[List[float]]: Результат умножения двух матриц.

    Исключения:
    ValueError: Если количество столбцов первой матрицы не совпадает с количеством строк второй матрицы.
    """
    if len(m1[0]) != len(m2):
        raise ValueError(
            "Количество столбцов первой матрицы должно совпадать с количеством строк второй матрицы."
        )

    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*m2)] for row in m1]


def transpose_matrix(m: List[List[float]]) -> List[List[float]]:
    """
    Транспонирует матрицу.

    Параметры:
    m (List[List[float]]): Исходная матрица.

    Возвращает:
    List[List[float]]: Транспонированная матрица.
    """
    return list(map(list, zip(*m)))
