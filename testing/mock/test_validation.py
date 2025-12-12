import pytest
from validation_utils import is_valid_score
import math
import numpy as np
import pandas as pd

# The decorator takes two main arguments:
# 1. A comma-separated string of argument names (matching the test function's arguments)
# 2. An iterable (usually a list of tuples) of the parameter values
@pytest.mark.parametrize(
    "input_score, expected_is_valid", 
    [
        # --- Valid Scores ---
        (10, True),             # Basic positive integer
        (0, True),              # Boundary condition (zero)
        (99.9, True),           # Positive float
        
        # --- Invalid Scores (Edge Cases) ---
        (-5, False),            # Negative number
        (None, False),          # Missing value
        ("100", False),         # Wrong data type (string)
        
        # --- Special Numerical Cases (Data Science Specific) ---
        (float('inf'), True),   # Infinity (usually considered valid if positive)
        (float('-inf'), False), # Negative infinity
        (np.nan, False),        # NaN (Not a Number)
        (pd.NA, False),         # Pandas missing value
    ]
)
def test_is_valid_score_cases(input_score, expected_is_valid):
    """
    Tests the is_valid_score function with a variety of data inputs.
    """
    # ACT & ASSERT are combined in a single line
    actual_result = is_valid_score(input_score)
    assert actual_result == expected_is_valid