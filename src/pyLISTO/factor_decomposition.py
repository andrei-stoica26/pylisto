from __future__ import annotations

from math import prod
from typing import List, Optional


def generate_primes(max: int) -> List[int]:
    """
    Generate all prime numbers less than or equal to `max`
    using the Sieve of Eratosthenes.
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


def factorial_prime_powers(n: int) -> Optional[List[int]]:
    """
    Generate the prime factor decomposition of n factorial.

    Args:
        n: A non-negative integer.

    Returns:
        A list where positions correspond to prime numbers
        (2, 3, 5, 7, ...) and values correspond to their
        exponents in the decomposition of n!.

        Returns None for n = 0 or n = 1.

    Example:
        factorial_prime_powers(8)
        # Returns [7, 2, 1, 1]
        # Corresponding to:
        # 2^7 * 3^2 * 5^1 * 7^1
    """
    if n in (0, 1):
        return None

    if n < 0:
        raise ValueError("`n` must be a non-negative integer.")

    primes = generate_primes(max=n)
    result: List[int] = [0] * len(primes)

    for i, prime in enumerate(primes):
        k = prime

        while k <= n:
            result[i] += n // k
            k *= prime

    return result


def power_product(primes: List[int], exponents: List[int]) -> int:
    """
    Compute the product of primes raised to their exponents.

    Args:
        primes: List of prime numbers.
        exponents: Corresponding exponents.

    Returns:
        The integer product:
            prod(prime_i ** exponent_i)

    Example:
        power_product([2, 3, 5], [4, 2, 6])
    """
    if len(primes) != len(exponents):
        raise ValueError("`primes` and `exponents` must have the same length.")

    return prod(p**e for p, e in zip(primes, exponents))