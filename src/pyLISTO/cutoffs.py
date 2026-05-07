from __future__ import annotations

from typing import Optional, Union

import numpy as np
import pandas as pd


ObjectType = Union[pd.DataFrame, list[str]]


def get_object_values(
    obj: ObjectType,
    num_col: Optional[str] = None,
    is_high_top: bool = True,
) -> Union[np.ndarray, float]:
    """
    Extract numeric values from an input object.

    Args:
        obj:
            A pandas DataFrame with a numeric column or a list of strings.
        num_col:
            The name of the numeric column used for DataFrame ordering.
        is_high_top:
            Whether higher values in the numeric column correspond to
            better-ranked items.

    Returns:
        A NumPy array of numeric values, or +/- infinity for string-list
        inputs or when `num_col` is None.
    """
    if num_col is None or isinstance(obj, list):
        return -np.inf if is_high_top else np.inf

    return obj[num_col].to_numpy()


def generate_cutoffs(
    obj1: ObjectType,
    obj2: ObjectType,
    obj3: Optional[ObjectType] = None,
    num_col: Optional[str] = None,
    is_high_top: bool = True,
    max_cutoffs: int = 5000,
) -> np.ndarray:
    """
    Generate cutoffs for filtering overlaps.

    Args:
        obj1:
            A pandas DataFrame with a numeric column or a list of strings.
        obj2:
            A pandas DataFrame with a numeric column or a list of strings.
        obj3:
            An optional pandas DataFrame with a numeric column or a list
            of strings.
        num_col:
            The name of the numeric column used for DataFrame ordering.
        is_high_top:
            Whether higher values in the numeric column correspond to
            better-ranked items.
        max_cutoffs:
            Maximum number of cutoffs.

    Returns:
        A NumPy array of cutoff values.
    """
    values1 = get_object_values(obj1, num_col, is_high_top)
    values2 = get_object_values(obj2, num_col, is_high_top)

    if obj3 is None:
        values3 = values2
        cutoffs = np.unique(np.concatenate([values1, values2]))
    else:
        values3 = get_object_values(obj3, num_col, is_high_top)
        cutoffs = np.unique(np.concatenate([values1, values2, values3]))

    if is_high_top:
        bound = min(np.max(values1), np.max(values2), np.max(values3))
        cutoffs = cutoffs[cutoffs < bound]
    else:
        bound = max(np.min(values1), np.min(values2), np.min(values3))
        cutoffs = cutoffs[cutoffs > bound]

    cutoffs = np.sort(cutoffs)

    if is_high_top:
        cutoffs = cutoffs[::-1]

    extra_cutoff = -np.inf if is_high_top else np.inf
    cutoffs = np.unique(np.append(cutoffs, extra_cutoff))

    n_cutoffs = len(cutoffs)

    if n_cutoffs > max_cutoffs:
        print(
            f"{n_cutoffs} cutoffs found in the input data frames. "
            f"Only {max_cutoffs} will be used. "
            "To change this behavior, set a higher value to "
            "`max_cutoffs`."
        )

        indices = np.linspace(
            0,
            n_cutoffs - 1,
            num=max_cutoffs,
            dtype=int,
        )
        cutoffs = cutoffs[indices]

    return cutoffs