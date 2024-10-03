import math
from typing import List


def scalar_multiply(v1: List[float], v2: List[float]) -> float:
    """
    Calculates the scalar product of two vectors.

    Parameters:
    v1 (List[float]): The first vector.
    v2 (List[float]): The second vector.

    Returns:
    float: The scalar product of two vectors.

    Exceptions:
    ValueError: If the dimensions of the vectors do not match
    """
    if len(v1) != len(v2):
        raise ValueError("The dimensions of the vectors must match.")

    return sum(x * y for x, y in zip(v1, v2))


def vector_length(v: List[float]) -> float:
    """
    Calculates the length (norm) of the vector.

    Parameters:
    v (List[float]): Vector.

    Returns:
    float: The length of the vector.

    Exceptions:
    ValueError: If the vector is empty.
    """
    if not v:
        raise ValueError("The vector must not be empty.")

    return math.sqrt(scalar_multiply(v, v))


def angle_vectors(v1: List[float], v2: List[float]) -> float:
    length_v1 = vector_length(v1)
    length_v2 = vector_length(v2)

    if length_v1 == 0 or length_v2 == 0:
        raise ValueError(
            "The length of one of the vectors is zero, the angle cannot be determined."
        )

    # Вычисление скалярного произведения
    dot_product = scalar_multiply(v1, v2)
    # Убедитесь, что значение cos_angle не выходит за пределы [-1, 1]
    cos_angle = dot_product / (length_v1 * length_v2)
    cos_angle = max(-1.0, min(1.0, cos_angle))

    return math.acos(cos_angle)
