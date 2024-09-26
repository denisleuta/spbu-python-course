import math
from typing import List

def matrix_addition(m1: List[List[float]], m2: List[List[float]]) -> List[List[float]]:
    return [[x + y for x, y in zip(row1, row2)] for row1, row2 in zip(m1, m2)]

def matrix_multiply(m1: List[List[float]], m2: List[List[float]]) -> List[List[float]]:
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*m2)] for row in m1]

def transpose_matrix(m: List[List[float]]) -> List[List[float]]:
    return list(map(list, zip(*m)))
    
