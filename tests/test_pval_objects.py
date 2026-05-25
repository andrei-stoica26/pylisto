import pytest
import pylisto as pyl
from string import ascii_uppercase


def test_pval_objects():
    letters = list(ascii_uppercase)

    res = pyl.pval_objects(
        letters[1:7],
        letters[2:19],
        universe1=letters,
    )
    assert res == pytest.approx(0.2956522, abs=1e-4)

    res = pyl.pval_objects(
        letters[1:7],
        letters[2:19],
        letters,
        letters[3:8],
        type="3N",
    )
    assert res == pytest.approx(0.0007643267, abs=1e-4)

    res = pyl.pval_objects(
        letters[1:7],
        letters[2:8],
        universe1=letters[:16],
        universe2=letters[1:26],
        type="2MN",
    )
    assert res == pytest.approx(0.01098901, abs=1e-4)
