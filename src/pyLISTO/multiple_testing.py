from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd
from numpy.typing import ArrayLike, NDArray
from statsmodels.stats.multitest import multipletests


def bf_correct_v(
    pvals: ArrayLike,
    n_comp: int,
) -> NDArray[np.float64]:
    """
    Perform Bonferroni correction on a vector of p-values.

    Parameters
    ----------
    pvals : array-like
        Numeric vector of p-values.
    n_comp : int
        Number of comparisons.

    Returns
    -------
    np.ndarray
        Bonferroni-adjusted p-values.
    """
    pvals_array: NDArray[np.float64] = np.asarray(pvals, dtype=float)
    return np.minimum(pvals_array * n_comp, 1.0)


def mt_correct_helper(
    pvals: ArrayLike,
    mt_method: str = "fdr_by",
    n_comp: int | None = None,
) -> NDArray[np.float64]:
    """
    Helper function for multiple comparison testing.

    Parameters
    ----------
    pvals : array-like
        Numeric vector of p-values.
    mt_method : str
        Multiple testing method.
    n_comp : int or None
        Number of comparisons.

    Returns
    -------
    np.ndarray
        Adjusted p-values.
    """
    pvals_array: NDArray[np.float64] = np.asarray(pvals, dtype=float)

    if n_comp is None:
        n_comp = len(pvals_array)

    mt_methods: list[str] = [
        "bonferroni",
        "sidak",
        "holm-sidak",
        "holm",
        "simes-hochberg",
        "hommel",
        "fdr_bh",
        "fdr_by",
        "fdr_tsbh",
        "fdr_tsbky",
    ]

    if mt_method not in mt_methods:
        raise ValueError(f"Unsupported mt_method: {mt_method}")

    if n_comp >= len(pvals_array):
        return multipletests(
            pvals_array,
            alpha=0.05,
            method=mt_method,
        )[1]

    if mt_method == "bonferroni":
        return bf_correct_v(pvals_array, n_comp)

    raise ValueError(
        "`n_comp` can be greater than the number of rows "
        "only if `mt_method` is set to 'bonferroni'."
    )


def mt_correct_v(
    pvals: ArrayLike,
    mt_method: str = "fdr_by",
    mt_stat: str = "identity",
    n_comp: int | None = None,
) -> NDArray[np.float64] | float:
    """
    Perform multiple testing correction on a vector of p-values.

    Parameters
    ----------
    pvals : array-like
        Numeric vector of p-values.
    mt_method : str
        Multiple testing correction method.
    mt_stat : str
        Summary statistic to return:
        'identity', 'median', 'mean', 'max', 'min'
    n_comp : int or None
        Number of comparisons.

    Returns
    -------
    np.ndarray or float
        Adjusted p-values or summary statistic.

    Examples
    --------
    >>> mt_correct_v([0.032, 0.001, 0.0045, 0.051, 0.048])
    array([0.11645   , 0.01141667, 0.0256875 , 0.11645   , 0.11645   ])

    >>> mt_correct_v([0.032, 0.001, 0.0045], mt_stat="median")
    0.011416666666666666
    """
    adjusted: NDArray[np.float64] = mt_correct_helper(
        pvals=pvals,
        mt_method=mt_method,
        n_comp=n_comp,
    )

    stat_map: dict[
        str,
        Callable[[NDArray[np.float64]], NDArray[np.float64] | float],
    ] = {
        "identity": lambda x: x,
        "median": np.median,
        "mean": np.mean,
        "max": np.max,
        "min": np.min,
    }

    if mt_stat not in stat_map:
        raise ValueError(f"Unsupported mt_stat: {mt_stat}")

    return stat_map[mt_stat](adjusted)


def mt_correct_df(
    df: pd.DataFrame,
    mt_method: str = "fdr_by",
    col_str: str = "pval",
    new_col_str: str = "pvalAdj",
    pval_thr: float | None = 0.05,
    do_order: bool = True,
    n_comp: int | None = None,
) -> pd.DataFrame:
    """
    Perform multiple testing correction on a DataFrame column.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing p-values.
    mt_method : str
        Multiple testing correction method.
    col_str : str
        Name of p-value column.
    new_col_str : str
        Name of adjusted p-value column.
    pval_thr : float or None
        Filtering threshold (None disables filtering).
    do_order : bool
        Whether to sort by adjusted p-values.
    n_comp : int or None
        Number of comparisons.

    Returns
    -------
    pandas.DataFrame
        Updated DataFrame.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     "elem": ["A", "B", "C", "D", "E"],
    ...     "pval": [0.032, 0.001, 0.0045, 0.051, 0.048]
    ... })
    >>> mt_correct_df(df)
      elem   pval  pvalAdj
    0    B  0.001   0.011417
    1    C  0.0045  0.025688
    2    A  0.032   0.11645
    3    D  0.051   0.11645
    4    E  0.048   0.11645
    """
    df = df.copy()

    if n_comp is None:
        n_comp = len(df)

    df[new_col_str] = mt_correct_v(
        df[col_str].values,
        mt_method=mt_method,
        mt_stat="identity",
        n_comp=n_comp,
    )

    if pval_thr is not None:
        df = df[df[new_col_str] < pval_thr]

    if do_order:
        df = df.sort_values(new_col_str)

    return df.reset_index(drop=True)