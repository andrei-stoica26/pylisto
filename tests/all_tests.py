import numpy as np
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
    assert pyl.cutoffs.get_object_values(df, "cost") == [6, 5, 3]
    assert pyl.cutoffs.get_object_values(df, None) == float("-inf")
    assert pyl.cutoffs.get_object_values(letters, "cost", False) == float("inf")

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
    assert list(res) == [5, 4, 3, 1, -np.inf]

    v1 = ["banana", "apple", "sour cherry", "lemon", "pineapple"]
    

def test_factorization_functions():
    assert pyl.factorial_prime_powers(8) == [7, 2, 1, 1]
    assert pyl.power_product([2, 3, 5], [4, 2, 6]) == 2250000

def test_prob_counts_2mn():
    res = pyl.prob_counts_2mn(300, 70, 110, 6)
    assert res == pytest.approx(2.091706e-09, rel=1e-4, abs=1e-4)

    res = sum(
        pyl.prob_counts_2mn(300, 70, 110, i)
        for i in range(0, 71)
    )
    assert res == pytest.approx(1, rel=1e-4, abs=1e-4)

def test_prob_counts_3n():
    res = pyl.prob_counts_3n(25, 20, 30, 140, 8)
    assert res == pytest.approx(6.875155e-08, rel=1e-4, abs=1e-4)

    res = sum(
        pyl.prob_counts_3n(25, 20, 30, 140, i)
        for i in range(0, 21)
    )
    assert res == pytest.approx(1, rel=1e-4, abs=1e-4)

def test_pval_counts_functions():
    res = pyl.pval_counts_2mn(300, 23, 24, 6)
    assert res == pytest.approx(0.005571074, rel=1e-4, abs=1e-4)

    res = pyl.pval_counts_3n(300, 200, 250, 400, 180)
    assert res == pytest.approx(5.101079e-62, rel=1e-4, abs=1e-4)

#def test_pval_objects():
    #letters = list(ascii_uppercase)
    #res = pyl.pval_objects(letters[2:8], letters[3:20], universe1=letters)