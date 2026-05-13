from typing import Callable, Optional, Union, List
import pandas as pd


def filter_items(
    obj: Union[List[str], pd.DataFrame],
    num_col: Optional[str] = None,
    cutoff: Optional[float] = None,
    comp_fun: Callable = lambda x, y: x > y,
) -> Union[List[str], List[str]]:
    """
    Filter items based on a provided cutoff.

    This function filters items based on a provided cutoff value.

    - If `obj` is a list of strings, it is returned unchanged.
    - If `obj` is a pandas DataFrame, rows are filtered based on a comparison
      function applied to a numeric column, and the row index is returned.

    Args:
        obj:
            Either a list of strings or a pandas DataFrame.
        num_col:
            Name of the numeric column used for filtering. Required if obj is
            a DataFrame.
        cutoff:
            Cutoff value used for comparison.
        comp_fun:
            Comparison function applied elementwise to `obj[num_col]` and
            `cutoff`. Defaults to greater-than.

    Returns:
        If `obj` is a list of strings, returns it unchanged.
        If `obj` is a DataFrame, returns a list of row index labels that
        satisfy the filter condition.

    Raises:
        ValueError:
            If `obj` is a DataFrame and `num_col` is not provided.
        KeyError:
            If `num_col` is not found in the DataFrame.
    """
    # Case 1: list of strings -> no filtering
    if isinstance(obj, list):
        return obj

    # Case 2: DataFrame filtering
    if num_col is None:
        raise ValueError("`num_col` must be provided when obj is a DataFrame.")

    if num_col not in obj.columns:
        raise KeyError(f"Column '{num_col}' not found in DataFrame.")

    mask = comp_fun(obj[num_col], cutoff)
    filtered = obj[mask]

    return list(filtered.index)