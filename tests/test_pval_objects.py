import numpy as np
import pandas as pd
import pylisto as pyl
import pytest
from string import ascii_uppercase
    

def test_pval_counts_functions():
    res = pyl.pval_counts_2mn(300, 23, 24, 6)
    assert res == pytest.approx(0.005571074, rel=1e-4, abs=1e-4)

    res = pyl.pval_counts_3n(300, 200, 250, 400, 180)
    assert res == pytest.approx(5.101079e-62, rel=1e-4, abs=1e-4)

#def test_pval_objects():
    #letters = list(ascii_uppercase)
    #res = pyl.pval_objects(letters[2:8], letters[3:20], universe1=letters)
