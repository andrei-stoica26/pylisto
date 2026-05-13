from scipy.stats import hypergeom
from typing import List


from pval_counts import pval_counts_2mn, pval_counts_3n


def pval_sets_2n(
    a: list[str],
    b: list[str],
    n: list[str]
) -> float:
    """
    Calculate the p-value of intersection for two sets.

    This function computes the probability of observing at least the
    current overlap between two subsets using the hypergeometric
    distribution.

    Parameters
    ----------
    a : list[str]
        First subset.
    b : list[str]
        Second subset.
    n : list[str]
        Set from which `a` and `b` are selected.

    Returns
    -------
    float
        A numeric value in [0, 1] representing the p-value of
        intersection for two sets.


    Examples
    --------
    >>> pval_sets_2n(
    ...     ["D", "E", "F", "G", "H", "I", "J"],
    ...     ["G", "H", "I", "J", "K", "L", "M", "N", "O"],
    ...     list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    ... )
    """
    na: int = len(a)
    nb: int = len(b)
    n_shared: int = len(set(a).intersection(set(b)))
    nn: int = len(n)

    return float(
        hypergeom.sf(
            n_shared - 1,
            nn,
            na,
            nb
        )
    )


def pval_sets_2mn(
    a: List[str],
    b: List[str],
    m: List[str],
    n: List[str],
) -> float:
    """
    Compute the p-value of the intersection of two subsets of sets M and N.

    This function computes the p-value of intersection between two subsets
    ``a`` and ``b``, where ``a`` is selected from set ``m`` and ``b`` is
    selected from set ``n``.

    It is a thin wrapper around ``pval_counts_2mn``.

    Args:
        a:
            Subset selected from ``m``.
        b:
            Subset selected from ``n``.
        m:
            Set from which ``a`` is selected.
        n:
            Set from which ``b`` is selected.

    Returns:
        A numeric value in the range [0, 1] representing the p-value of the
        intersection of the two subsets.

    Raises:
        ValueError:
            If ``a`` is not a subset of ``m``.
        ValueError:
            If ``b`` is not a subset of ``n``.

    Example:
        >>> pval_sets_2mn(
        ...     ["D", "E", "F", "G", "H", "I", "J"],
        ...     ["G", "H", "I", "J", "K", "L", "M", "N", "O"],
        ...     list("ABCDEFGHIJKLMNOPQRS"),
        ...     list("FGHIJKLMNOPQRSTUVWXYZ"),
        ... )
    """
    set_a = set(a)
    set_b = set(b)
    set_m = set(m)
    set_n = set(n)

    if set_a - set_m:
        raise ValueError("`a` must be a subset of `m`.")

    if set_b - set_n:
        raise ValueError("`b` must be a subset of `n`.")

    return pval_counts_2mn(
        len(set_m & set_n),
        len(set_a & set_n),
        len(set_b & set_m),
        len(set_a & set_b),
    )


def pval_sets_3n(
    a: List[str],
    b: List[str],
    c: List[str],
    n: List[str],
) -> float:
    """
    Compute the p-value of the intersection of three subsets.

    This function computes the p-value of the intersection of three subsets
    ``a``, ``b``, and ``c``, where all three are selected from the set ``n``.

    It is a thin wrapper around ``pval_counts_3n``.

    Args:
        a:
            First subset selected from ``n``.
        b:
            Second subset selected from ``n``.
        c:
            Third subset selected from ``n``.
        n:
            Set from which ``a``, ``b``, and ``c`` are selected.

    Returns:
        A numeric value in the range [0, 1] representing the p-value of the
        intersection of the three subsets.

    Raises:
        ValueError:
            If ``a`` is not a subset of ``n``.
        ValueError:
            If ``b`` is not a subset of ``n``.
        ValueError:
            If ``c`` is not a subset of ``n``.

    Example:
        >>> pval_sets_3n(
        ...     ["D", "E", "F", "G", "H", "I", "J"],
        ...     ["G", "H", "I", "J", "K", "L", "M", "N", "O"],
        ...     list("ABCDEFGHIJKLMNOPQRS"),
        ...     list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        ... )
    """
    set_a = set(a)
    set_b = set(b)
    set_c = set(c)
    set_n = set(n)

    if set_a - set_n:
        raise ValueError("`a` must be a subset of `n`.")

    if set_b - set_n:
        raise ValueError("`b` must be a subset of `n`.")

    if set_c - set_n:
        raise ValueError("`c` must be a subset of `n`.")

    intersection_size = len(set_a & set_b & set_c)

    return pval_counts_3n(
        len(a),
        len(b),
        len(c),
        len(n),
        intersection_size,
    )