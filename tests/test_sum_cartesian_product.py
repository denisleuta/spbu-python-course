import pytest
import sys
import os
from typing import Tuple

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.sum_cartesian_product import sum_cartesian_product


def test_sum_cartesian_product() -> None:
    """
    Test the parallel computation of the sum of the Cartesian product for multiple sets of integers.
    """
    sets = [
        [1, 2],  # First set
        [3, 4],  # Second set
        [5, 6],  # Third set
    ]

    result = sum_cartesian_product(sets)

    # Expected sum of the Cartesian product
    expected_sum = (
        sum([1, 3, 5])
        + sum([1, 3, 6])
        + sum([1, 4, 5])
        + sum([1, 4, 6])
        + sum([2, 3, 5])
        + sum([2, 3, 6])
        + sum([2, 4, 5])
        + sum([2, 4, 6])
    )

    assert result == expected_sum, f"Expected {expected_sum}, but got {result}"
