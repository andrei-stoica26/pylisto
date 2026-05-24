import pylisto as pyl
import pytest


def test_vector_functions_work():
    res = pyl.v_sum(
        [1, 4],
        [2, 8, 6],
        [1, 7],
        [10, 4, 6, 7],
    )
    assert res == [14, 23, 12, 7]

    res = pyl.v_choose(8, 4)
    assert res == [1, 0, 1, 1]

    res = pyl.vectors.v_numerator_mn(20, 8, 6, 2)
    assert res == [2, 2, 1, 1, 1]