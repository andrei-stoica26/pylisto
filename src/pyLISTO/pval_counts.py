from vectors import v_sum, v_choose, v_numerator_mn
from sympy import prime


from .factor_decomposition import power_product


def pval_counts_2mn(
    int_mn: int,
    int_an: int,
    int_bm: int,
    k: int
) -> float:
    """
    Compute the probability that two subsets of sets M and N intersect
    in at least k points.

    Args:
        int_mn:
            Size of the intersection between sets M and N.
        int_an:
            Size of the intersection between subset A and set N.
        int_bm:
            Size of the intersection between subset B and set M.
        k:
            Minimum required size of the intersection between subsets A and B.

    Returns:
        Probability value in [0, 1].

    Example:
       >>>  pval_counts_2mn (300, 23, 24, 6)
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


def pval_counts_3n(
    len_a: int,
    len_b: int,
    len_c: int,
    n: int,
    k: int
) -> float:
    """
    Compute the probability that three subsets of a set intersect
    in at least k points.

    Args:
        len_a:
            Size of the first subset.
        len_b:
            Size of the second subset.
        len_c:
            Size of the third subset.
        n:
            Size of the set comprising the subsets.
        k:
            Minimum size of the intersection.
        
    Returns:
        A numeric value in [0, 1] representing the probability that
        three subsets of a set intersect in at least k points.

    Raises:
        ValueError:
            If `k` exceeds the minimum length of the three subsets.

    Example:
        >>> pval_counts_3n(300, 200, 250, 400, 180)
    """
    if k == 0:
        return 1.0

    lengths = sorted([len_a, len_b, len_c])

    if k > lengths[0]:
        raise ValueError(
            "`k` must not exceed the minimum length of the three sets."
        )

    pval: float = 0.0

    for x in range(k, lengths[0] + 1):
        pval += prob_counts_3n(
            lengths[0],
            lengths[1],
            lengths[2],
            n,
            x
        )

    return pval