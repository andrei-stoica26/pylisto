from typing import List
from vectors import v_sum, v_choose, v_numerator_mn
from sympy import prime
from .factor_decomposition import power_product

def prob_counts_2mn(
    int_mn: int,
    int_an: int,
    int_bm: int,
    k: int
) -> float:
    """
    Compute the probability that two subsets of sets M and N intersect in k points.

    This function computes the probability that two subsets of sets M and N
    intersect in exactly k points. The required intersection sizes
    (M ∩ N, A ∩ N, and B ∩ M) must be provided.

    Parameters
    ----------
    int_mn : int
        Size of the intersection between sets M and N.
    int_an : int
        Size of the intersection between sets A and N.
    int_bm : int
        Size of the intersection between sets B and M.
    k : int
        Desired intersection size.

    Returns
    -------
    float
        Probability that two subsets of sets M and N intersect in k points.

    Example
        >>> prob_counts_2mn(8, 6, 4, 2)
        30

    """

    exponents: List[int] = v_sum(
        v_numerator_mn(int_mn, int_an, int_bm, k),
        -1 * v_choose(int_mn, int_bm)
    )

    primes: List[int] = [prime(i) for i in range(1, len(exponents) + 1)]

    return power_product(primes, exponents)
