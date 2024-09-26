import pytest
import math

import sys
import os

sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))
from project.vector_operations import scalar_multyply, vector_length, angle_vectors

def test_scalar_multyply():
    assert scalar_multyply([1, 2, 3], [4, 5, 6]) == 32

def test_vector_length():
    assert vector_length([3, 4]) == 5

def test_angle_vectors():
    assert pytest.approx(angle_vectors([1, 0], [0, 1])) == math.pi / 2

