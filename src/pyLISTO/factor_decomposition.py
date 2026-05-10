from __future__ import annotations
from math import prod
from typing import List, Optional
from sympy import primerange


def factorial_prime_powers(n: int) -> Optional[List[int]]:
    """
    Prime factor exponents of n! corresponding to primes (2, 3, 5, 7, ...).

    Returns:
        List of exponents in order of primes, or None for n = 0 or 1.

    Example:
        >>> factorial_prime_powers(8)
        [7, 2, 1, 1]

    """
    if n in (0, 1):
        return None
    if n < 0:
        raise ValueError("n must be a non-negative integer.")

    primes = list(primerange(1, n))
    result: List[int] = [0] * len(primes)

    for i, prime in enumerate(primes):
        k = prime
        while k <= n:
            result[i] += n // k
            k *= prime

    return result


def power_product(primes: List[int], exponents: List[int]) -> int:
    """
    Compute product of primes raised to their exponents.

    Args:
        primes: List of primes.
        exponents: Corresponding exponents.

    Returns:
        Integer result of Π(prime_i ** exponent_i)

    Example:
        >>> power_product([2, 3, 5], [4, 2, 6])
        155520

    """
    if len(primes) != len(exponents):
        raise ValueError("primes and exponents must have the same length.")

    return prod(p**e for p, e in zip(primes, exponents))