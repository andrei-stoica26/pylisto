from vectors import v_sum, v_choose, v_numerator_mn
from sympy import prime
from factor_decomposition import power_product


def pval_counts_2mn(
    int_mn: int,
    int_an: int,
    int_bm: int,
    k: int
) -> float:
    """
    Compute the probability that two subsets of sets M and N intersect
    in at least k points.

    Parameters
    ----------
    int_mn : int
        Size of the intersection between sets M and N.
    int_an : int
        Size of the intersection between subset A and set N.
    int_bm : int
        Size of the intersection between subset B and set M.
    k : int
        Minimum required size of the intersection between subsets A and B.

    Returns
    -------
    float
        Probability value in [0, 1].
    """
    denom = -1 * v_choose(int_mn, int_bm)
    pval: float = 0.0

    for i in range(k, min(int_an, int_bm) + 1):
        exponents = v_sum(
            v_numerator_mn(int_mn, int_an, int_bm, i),
            denom
        )
        primes: List[int] = [prime(i) for i in range(1, len(exponents) + 1)]
        pval += power_product(primes, exponents)

    return pval