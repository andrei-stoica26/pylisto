from __future__ import annotations

from typing import Optional, Union

import numpy as np
import pandas as pd


ObjectType = Union[pd.DataFrame, list[str]]


def get_object_values(
    obj: pd.DataFrame | list[str] | None,
    num_col: str | None,
) -> pd.Series | list[float]:
    """
    Extract numeric values from an input object.

    If ``obj`` is ``None``, ``num_col`` is ``None``, or ``obj`` is a list of
    strings, returns ``[-inf, inf]``. Otherwise, returns the specified column
    from the DataFrame.

    Args:
        obj: A pandas DataFrame containing a numeric column, a list of strings,
            or ``None``.
        num_col: Name of the numeric column to extract.

    Returns:
        The values from ``obj[num_col]`` if a valid DataFrame and column name
        are provided; otherwise ``[-inf, inf]``.
    """
    if obj is None or num_col is None or isinstance(obj, list):
        return [float("-inf"), float("inf")]

    return obj[num_col]


def generate_cutoffs(
    obj1: pd.DataFrame | list[str] | None,
    obj2: pd.DataFrame | list[str] | None,
    obj3: pd.DataFrame | list[str] | None = None,
    num_col: str | None = None,
    is_high_top: bool = True,
    max_cutoffs: int = 500,
) -> np.ndarray:
    """
    Generate cutoffs for filtering overlaps.

    Args:
        obj1: A DataFrame containing a numeric column, a list of strings,
            or ``None``.
        obj2: A DataFrame containing a numeric column, a list of strings,
            or ``None``.
        obj3: A DataFrame containing a numeric column, a list of strings,
            or ``None``.
        num_col: Name of the numeric column used to generate cutoffs.
        is_high_top: Whether higher numeric values correspond to better-ranked
            items.
        max_cutoffs: Maximum number of cutoffs to return. If more cutoffs are
            generated, a linearly spaced subset is selected.

    Returns:
        A NumPy array of cutoff values.
    """
    values1 = np.asarray(get_object_values(obj1, num_col))
    values2 = np.asarray(get_object_values(obj2, num_col))
    values3 = np.asarray(get_object_values(obj3, num_col))

    cutoffs = np.unique(np.concatenate([values1, values2, values3]))

    if is_high_top:
        bound = min(values1.max(), values2.max(), values3.max())
        cutoffs = cutoffs[cutoffs < bound]
    else:
        bound = max(values1.min(), values2.min(), values3.min())
        cutoffs = cutoffs[cutoffs > bound]

    cutoffs = np.sort(cutoffs)
    if is_high_top:
        cutoffs = cutoffs[::-1]

    n_cutoffs = len(cutoffs)
    if n_cutoffs > max_cutoffs:
        indices = np.linspace(
            0,
            n_cutoffs - 1,
            num=max_cutoffs,
            dtype=int,
        )
        cutoffs = cutoffs[indices]

    return cutoffs