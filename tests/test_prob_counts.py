import pylisto as pyl
import pytest
    
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

