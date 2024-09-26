import math
from typing import List

def scalar_multyply(v1: List[float], v2: List[float]) -> float:
    return sum(x * y for x, y in zip(v1, v2))

def vector_length(v: List[float]) -> float:
    return math.sqrt(scalar_multyply(v, v))

def angle_vectors(v1: List[float], v2: List[float]) -> float:
    return math.acos(scalar_multyply(v1, v2) / (vector_length(v1) * vector_length(v2)))
