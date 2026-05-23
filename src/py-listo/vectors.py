from __future__ import annotations
from typing import List, Optional
from math import prod

from .factor_decomposition import factorial_prime_powers


def v_sum(*vectors: List[int]) -> List[int]:
    """
    Add numeric vectors of different lengths by zero-padding shorter ones.

    Args:
        vectors:
            Variable number of integer lists representing vectors.

    Returns:
        A list of integers representing the element-wise sum of all input
        vectors, after zero-padding to equal length.

    Example:
    
        >>> v_sum([1, 4], [2, 8, 6])
    """
    if not vectors:
        return []

    max_len = max(len(v) for v in vectors)

    padded = [
        v + [0] * (max_len - len(v))
        for v in vectors
    ]

    result = [0] * max_len
    for v in padded:
        for i, x in enumerate(v):
            result[i] += x

    return result


def v_choose(n: int, k: int) -> List[int]:
    """
    Prime factor decomposition of binomial coefficient C(n, k).

    Args:
        n:
            Total number of elements.
        k:
            Number of selected elements.

    Returns:
        A vector in which positions represent prime numbers (that is, the
        first position corresponds to 2, the second position corresponds to 3,
        the third position corresponds to 5, etc.) and values
        represent their exponents in the factorial decomposition.

    Examples:
        >>> v_choose(8, 4)
    """
    fn = factorial_prime_powers(n) or []
    fk = factorial_prime_powers(k) or []
    fnk = factorial_prime_powers(n - k) or []

    fk = [-x for x in fk]
    fnk = [-x for x in fnk]

    return v_sum(fn, fk, fnk)


def v_numerator_mn(int_mn: int, int_an: int, int_bm: int, k: int) -> List[int]:
    """
    Prime representation of numerator for intersection probability expression.

    Args:
        int_mn:
            Number of elements in the intersection of sets M and N.
        int_an:
            Number of elements in the intersection of sets A (subset of M) and N.
        int_bm:
            Number of elements in the intersection of sets B (subset of N) and M.
        k:
            Number of elements in the intersection of sets A and B.
    
    Returns:
        A vector containing the prime representation of the fraction representing 
        the probability that two subsets of sets M and N intersect in k points. 
        Positions represent prime numbers in order (2, 3, 5...), and values
        represent their exponents in the prime decomposition.
        
    Example:
        >>> v_numerator_mn(8, 4, 3, 1)
    """
    a = v_choose(int_an, k)
    b = v_choose(int_mn - int_an, int_bm - k)
    return v_sum(a, b)