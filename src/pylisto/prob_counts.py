from typing import List
from sympy import prime
from scipy.stats import hypergeom
import numpy as np


from .vectors import v_sum, v_choose, v_numerator_mn
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

    Args:
        int_mn:
            Size of the intersection between sets M and N.
        int_an:
            Size of the intersection between sets A and N.
        int_bm:
            Size of the intersection between sets B and M.
        k:
            Desired intersection size.

    Returns:
        Probability that two subsets of sets M and N intersect in k points.

    Example:
        >>> prob_counts_2mn(8, 6, 4, 2)

    """
    denom = v_choose(int_mn, int_bm)
    exponents: List[int] = v_sum(
        v_numerator_mn(int_mn, int_an, int_bm, k),
        [-x for x in denom]
    )

    primes: List[int] = [prime(i) for i in range(1, len(exponents) + 1)]

    return power_product(primes, exponents)


def prob_counts_3n(a: int, b: int, c: int, n: int, k: int) -> float:
    """
    Compute the probability that three subsets of given sizes intersect
    in exactly k points.

    Args:
        a:
            Size of the first subset.
        b:
            Size of the second subset.
        c:
            Size of the third subset.
        n:
            Size of the universal set.
        k:
            Size of the desired triple intersection.

    Returns:
        Probability in [0, 1] that the three subsets intersect in exactly k points.

    Example:
        >>> prob_counts_3n(8, 6, 10, 20, 3)
    """

    lower = max(a + b - n, k)
    upper = min(a, b, n + k - c)

    if lower > upper:
        return 0.0

    x = np.arange(lower, upper + 1)

    p_x = hypergeom.pmf(x, n, a, b)
    p_k_given_x = hypergeom.pmf(k, n, x, c)

    return np.sum(p_x * p_k_given_x)