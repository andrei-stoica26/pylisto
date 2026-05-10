from __future__ import annotations
from typing import List


def generate_primes(max: int) -> List[int]:
    """
    Generate all prime numbers less than or equal to max using the Sieve of Eratosthenes.

    Args:
        max: Upper bound (inclusive).

    Returns:
        List of prime numbers ≤ max.

    Example:
        >>> generate_primes(10)
        [2, 3, 5, 7]

    """
    if max < 2:
        return []

    sieve = [True] * (max + 1)
    sieve[0] = sieve[1] = False

    for i in range(2, int(max**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, max + 1, i):
                sieve[j] = False

    return [i for i, is_prime in enumerate(sieve) if is_prime]
    