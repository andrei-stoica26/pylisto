from scipy.stats import hypergeom


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
    >>> pval_sets2_n(
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