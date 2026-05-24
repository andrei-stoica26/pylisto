import pandas as pd
import pytest
import pylisto as pyl


def test_multiple_testing_functions_work():
    pvals = [0.032, 0.001, 0.0045, 0.051, 0.048, 0.33]

    res = pyl.mt_correct_v(pvals)
    expected = [
        0.149940,
        0.014700,
        0.033075,
        0.149940,
        0.149940,
        0.808500,
    ]
    assert res == pytest.approx(expected, abs=1e-4)

    res = pyl.mt_correct_v(pvals, mt_method="fdr_bh", mt_stat="mean")
    assert res == pytest.approx(0.08885, abs=1e-4)

    res = pyl.mt_correct_v(pvals, mt_method="bonferroni", n_comp=4)
    expected = [0.128, 0.004, 0.018, 0.204, 0.192, 1.000]
    assert res == pytest.approx(expected)

    df = pd.DataFrame(
        {
            "elem": list("ABCDEF"),
            "pval": pvals,
        }
    )

    res = pyl.mt_correct_df(df)
    expected = [0.014700, 0.033075]
    assert list(res["pvalAdj"]) == pytest.approx(expected, abs=1e-4)

    res = pyl.mt_correct_df(df, mt_method="bonferroni", n_comp=3)
    expected = [0.0030, 0.0135]
    assert list(res["pvalAdj"]) == pytest.approx(expected, abs=1e-4)

    with pytest.raises(Exception):
        pyl.mt_correct_df(df, mt_method="holm", n_comp=3)
