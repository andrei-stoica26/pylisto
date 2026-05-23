import pandas as pd
import pylisto as pyl
import pytest
from string import ascii_uppercase

def test_checks():
    df1 = pd.DataFrame(
        {
            "fruit": ["apple", "banana", "cherry"],
            "cost": [6, 5, 3],
        }
    )

    df2 = pd.DataFrame(
        {
            "fruit": ["apple", "banana", "cherry"],
            "cost": ["6", "5", "3"],
        }
    )

    LETTERS = list(ascii_uppercase)

    pyl.checks.check_num_col(df1, "cost")
    pyl.checks.check_num_col(LETTERS, "cost")

    with pytest.raises(Exception):
        pyl.checks.check_num_col(df1, "price")

    with pytest.raises(Exception):
        pyl.checks.check_num_col(df2, "cost")

    pyl.checks.check_num_col_all([df1, LETTERS], "cost")
    pyl.checks.check_num_col_all([LETTERS, LETTERS], "cost")

    with pytest.raises(Exception):
        pyl.checks.check_num_col_all([df1, LETTERS], "price")

    with pytest.raises(Exception):
        pyl.checks.check_num_col_all([df2, LETTERS], "cost")
    