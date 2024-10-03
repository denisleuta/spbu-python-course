from typing import List


def matrix_addition(m1: List[List[float]], m2: List[List[float]]) -> List[List[float]]:
    """
    Adds two matrices.

    Parameters:
    m1 (List[List[float]]): The first matrix.
    m2 (List[List[float]]): The second matrix.

    Returns:
    List[List[float]]: The result of adding two matrices.

    Exceptions:
    ValueError: If the dimensions of the matrices do not match.
    """
    if len(m1) != len(m2) or any(len(row1) != len(row2) for row1, row2 in zip(m1, m2)):
        raise ValueError("The sizes of the matrices must match.")

    return [[x + y for x, y in zip(row1, row2)] for row1, row2 in zip(m1, m2)]


def matrix_multiply(m1: List[List[float]], m2: List[List[float]]) -> List[List[float]]:
    """
    Multiplies two matrices.

    Parameters:
    m1 (List[List[float]]): The first matrix.
    m2 (List[List[float]]): The second matrix.

    Returns:
    List[List[float]]: The result of multiplying two matrices.

    Exceptions:
    ValueError: If the number of columns of the first matrix does not match the number of rows of the second matrix.
    """
    if len(m1[0]) != len(m2):
        raise ValueError(
            "The number of columns of the first matrix must match the number of rows of the second matrix."
        )

    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*m2)] for row in m1]


def transpose_matrix(m: List[List[float]]) -> List[List[float]]:
    """
    Transposes the matrix.

    Parameters:
    m (List[List[float]]): The original matrix.

    Returns:
    List[List[float]]: The transposed matrix.
    """
    return list(map(list, zip(*m)))
