import numpy as np
import pandas as pd
import pylisto as pyl
import pytest
from string import ascii_uppercase
    

def test_pval_sets_functions():
    letters = list(ascii_uppercase)

    res = pyl.pval_sets_2n(
        letters[3:10],   
        letters[6:15], 
        letters,
    )
    assert res == pytest.approx(0.1585284, abs=1e-4)

    res = pyl.pval_sets_2mn(
        letters[3:10],  
        letters[6:15],  
        letters[:19],  
        letters[5:26],
    )
    assert res == pytest.approx(0.3776224, abs=1e-4)

    res = pyl.pval_sets_3n(
        letters[3:10],   
        letters[6:15],   
        letters[:19], 
        letters,
    )
    assert res == pytest.approx(0.05096209, abs=1e-4)
