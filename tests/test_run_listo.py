import pandas as pd
import pylisto as pyl
import pytest


def test_run_listo():
    universe1 = ["apple", "apricot", "banana", "blackberry", "blueberry", "cherry","chestnut", "fig", "grape", "grapefruit", 
    "hazelnut", "lemon", "lime", "orange", "mango", "melon", "nectarine", "peach", "peanut", "pineapple", "plum", "pomegranate", 
    "raspberry", "sour cherry", "walnut", "watermelon"]
    universe2 = ["banana", "coconut", "date", "lychee", "fig", "mango", "orange", "papaya", "passion fruit", "pineapple", "pomegranate"]

    dict1 = {
        "set11": pd.DataFrame(
            {"cost": [1.2, 0.8, 1.6, 1.9, 1.3]},
            index=["apple", "apricot", "cherry", "orange", "melon"],
            ),
        "set12": pd.DataFrame(
            {"cost": [2.6, 2.2, 1.8, 1.3, 1.4, 2.1, 2.2, 1.7]},
            index=["apricot", "banana", "fig", "plum", "pineapple", "pomegranate", "mango", "orange"],
        ),
    }

    dict2 = {
        "set21": pd.DataFrame(
            {"cost": [1.2, 0.8, 1.6, 1.8, 1.4, 0.3, 0.2]},
            index=["apple", "apricot", "cherry", "orange", "melon", "blueberry", "raspberry"],
        ),
        "set22": pd.DataFrame(
            {"cost": [1.3, 3.2, 2.1, 1.8, 1.7, 1.5, 1.8]},
            index=["apple", "banana", "fig", "orange", "pineapple", "plum", "pomegranate"],
        ),
    }

    dict3 = {
        "sig1": ["banana", "coconut", "mango", "pineapple", "pomegranate", "fig", "orange"],
        "sig2": ["banana", "fig", "mango", "orange"]
    }

    dict4 = {
        "newsig1": ["banana", "fig", "orange", "pomegranate"],
        "newsig2": ["apricot", "blackberry", "raspberry"]
    }

    res = pyl.run_listo(dict1, dict2, universe1=universe1, num_col='cost', verbose=False)
    val = list(res["pvalAdj"])[0]
    assert val == pytest.approx(0.013938, abs=1e-4)

    res = pyl.run_listo(dict1, dict3, universe1=universe1, universe2=universe2, num_col='cost', verbose=False)
    val = list(res["pvalAdj"])[0]
    assert val == pytest.approx(1, abs=1e-4)

    res = pyl.run_listo(dict1, dict2, dict4, universe1=universe1, num_col='cost', verbose=False)
    val = list(res["pvalAdj"])[0]
    assert val == pytest.approx(0.001764, abs=1e-4)
