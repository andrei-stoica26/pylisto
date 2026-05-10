from __future__ import annotations
from typing import List, Optional
from math import prod

from factor_decomposition import factorial_prime_powers


def v_sum(*vectors: List[int]) -> List[int]:
    """
    Add numeric vectors of different lengths by zero-padding shorter ones.

    Examples:
        >>> v_sum([1, 4], [2, 8, 6])
        [3, 12, 6]

        >>> v_sum([1, 7], [10, 4, 6, 7])
        [11, 11, 6, 7]
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

    Examples:
        >>> v_choose(5, 2)
        [1, 0, 1]

        >>> v_choose(8, 4)
        [1, 0, 1, 1]
    """
    fn = factorial_prime_powers(n) or []
    fk = factorial_prime_powers(k) or []
    fnk = factorial_prime_powers(n - k) or []

    fk = [-x for x in fk]
    fnk = [-x for x in fnk]

    return v_sum(fn, fk, fnk)


def v_numerator_mn(intMN: int, intAN: int, intBM: int, k: int) -> List[int]:
    """
    Prime representation of numerator for intersection probability expression.

    Examples:
        >>> v_numerator_mn(8, 4, 3, 1)
        [1, 1, 0, 0]
    """
    a = v_choose(intAN, k)
    b = v_choose(intMN - intAN, intBM - k)
    return v_sum(a, b)