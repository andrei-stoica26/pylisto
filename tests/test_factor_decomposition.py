import pylisto as pyl
import pytest
    
def test_factorization_functions():
    assert pyl.factorial_prime_powers(8) == [7, 2, 1, 1]
    assert pyl.power_product([2, 3, 5], [4, 2, 6]) == 2250000
