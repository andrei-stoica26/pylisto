from __future__ import annotations

import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests

def bf_correct_v(pvals, n_comp):
    """
    Perform Bonferroni correction on a vector of p-values.

    Unlike standard implementations, this allows n_comp to be smaller
    or larger than len(pvals), matching the R implementation.

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
    pvals = np.asarray(pvals, dtype=float)
    return np.minimum(pvals * n_comp, 1.0)

def mt_correct_helper(pvals, mt_method="fdr_by", n_comp=None):
    """
    Helper function for multiple comparison testing.

    Parameters
    ----------
    pvals : array-like
        Numeric vector of p-values.
    mt_method : str
        One of:
        'bonferroni', 'sidak', 'holm-sidak', 'holm', 'simes-hochberg', 
        'hommel', 'fdr_bh', 'fdr_by', 'fdr_tsbh', 'fdr_tsbky'
    n_comp : int or None
        Number of comparisons.

    Returns
    -------
    np.ndarray
        Adjusted p-values.
    """
    pvals = np.asarray(pvals, dtype=float)

    if n_comp is None:
        n_comp = len(pvals)

    mt_methods = ['bonferroni', 'sidak', 'holm-sidak', 'holm', 'simes-hochberg', 
        'hommel', 'fdr_bh', 'fdr_by', 'fdr_tsbh', 'fdr_tsbky']

    if mt_method not in mt_methods:
        raise ValueError(f"Unsupported mt_method: {mt_method}")

    if n_comp >= len(pvals):
        if mt_method == "none":
            return pvals.copy()

        adjusted = multipletests(
            pvals,
            alpha=0.05,
            method=mt_method
        )[1]
        return adjusted

    if mt_method == "bonferroni":
        return bf_correct_v(pvals, n_comp)

    raise ValueError(
        "`n_comp` can be greater than the number of rows "
        "only if `mt_method` is set to 'bonferroni'."
    )

def mt_correct_v(
    pvals,
    mt_method="fdr_by",
    mt_stat="identity",
    n_comp=None
):
    """
    Perform multiple testing correction on a vector of p-values.

    Parameters
    ----------
    pvals : array-like
        Numeric vector of p-values.
    mt_method : str
        One of:
        'bonferroni', 'sidak', 'holm-sidak', 'holm', 'simes-hochberg', 
        'hommel', 'fdr_bh', 'fdr_by', 'fdr_tsbh', 'fdr_tsbky'
    mt_stat : str
        One of:
        'identity', 'median', 'mean', 'max', 'min'
    n_comp : int or None
        Number of comparisons.

    Returns
    -------
    np.ndarray or float
        Adjusted p-values if mt_stat='identity',
        otherwise the requested summary statistic.
    """
    adjusted = mt_correct_helper(
        pvals=pvals,
        mt_method=mt_method,
        n_comp=n_comp
    )

    stat_map = {
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
    df,
    mt_method="fdr_by",
    col_str="pval",
    new_col_str="pvalAdj",
    pval_thr=0.05,
    do_order=True,
    n_comp=None
):
    """
    Perform multiple testing correction on a DataFrame column.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with a p-value column.
    mt_method : str
        Multiple testing correction method.
    col_str : str
        Name of p-value column.
    new_col_str : str
        Name of adjusted p-value column to create.
    pval_thr : float or None
        Threshold for filtering rows.
        If None, no filtering is performed.
    do_order : bool
        Whether to sort by adjusted p-values.
    n_comp : int or None
        Number of comparisons.

    Returns
    -------
    pandas.DataFrame
        Updated DataFrame.
    """
    df = df.copy()

    if n_comp is None:
        n_comp = len(df)

    df[new_col_str] = mt_correct_v(
        df[col_str].values,
        mt_method=mt_method,
        mt_stat="identity",
        n_comp=n_comp
    )

    if pval_thr is not None:
        df = df[df[new_col_str] < pval_thr]

    if do_order:
        df = df.sort_values(new_col_str)

    return df.reset_index(drop=True)

if __name__ == "__main__":
    pvals = [0.032, 0.001, 0.0045, 0.051, 0.048]

    print("Vector correction:")
    print(mt_correct_v(pvals))

    df = pd.DataFrame({
        "elem": ["A", "B", "C", "D", "E"],
        "pval": pvals
    })

    print("\nDataFrame correction:")
    print(mt_correct_df(df))

