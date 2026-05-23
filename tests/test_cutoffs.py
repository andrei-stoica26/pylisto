import pandas as pd
import pylisto as pyl
import pytest
from string import ascii_uppercase

def test_get_object_values():
    df = pd.DataFrame({
        "fruit": ["apple", "banana", "cherry"],
        "cost": [6, 5, 3]
    })
    letters = list(ascii_uppercase)
    assert list(pyl.cutoffs.get_object_values(df, "cost")) == [6, 5, 3]
    assert pyl.cutoffs.get_object_values(df, None) == [float("-inf"), float("inf")]
    assert pyl.cutoffs.get_object_values(letters, "cost") == [float("-inf"), float("inf")]

def test_generate_cutoffs():
    df1 = pd.DataFrame({
        "fruit": ["apple", "banana", "cherry", "plum", "orange"],
        "cost": [6, 5, 3, 4, 5]
    })
    df2 = pd.DataFrame({
        "fruit": ["watermelon", "grape", "banana", "apricot", "melon"],
        "cost": [8, 1, 4, 3, 6]
    })
    res = pyl.cutoffs.generate_cutoffs(df1, df2, num_col="cost")
    assert list(res) == [5, 4, 3, 1, float("-inf")]

    v1 = ["banana", "apple", "sour cherry", "lemon", "pineapple"]
    