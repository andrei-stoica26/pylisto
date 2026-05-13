from typing import Any, Callable, Iterable, Optional, Literal, Union, List
import pandas as pd


from pval_sets import pval_sets_2n, pval_sets_2mn, pval_sets_3n


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


def pval_objects_core(
    obj1: Union[List[str], pd.DataFrame],
    obj2: Union[List[str], pd.DataFrame],
    universe1: List[str],
    obj3: Optional[Union[List[str], pd.DataFrame]] = None,
    universe2: Optional[List[str]] = None,
    num_col: Optional[str] = None,
    cutoff: Optional[float] = None,
    comp_fun: Callable = lambda x, y: x > y,
    type: Literal["2N", "2MN", "3N"] = "2N",
) -> float:
    """
    Compute the p-value of overlap for two or three objects.

    This function:
    1. Filters input objects using `filter_items`
    2. Converts filtered results into sets of names
    3. Dispatches to the appropriate p-value function depending on `type`

    Args:
        obj1:
            First input object (list of strings or pandas DataFrame).
        obj2:
            Second input object (list of strings or pandas DataFrame).
        obj3:
            Optional third input object (required when type = "3N").
        universe1:
            Set from which items in obj1 are selected.
        universe2:
            Set from which items in obj2 are selected (required for "2MN").
        num_col:
            Column name used for filtering if DataFrame is provided.
        cutoff:
            Threshold used for filtering.
        comp_fun:
            Comparison function applied to numeric column and cutoff.
        type:
            Type of computation: "2N", "2MN", or "3N".

    Returns:
        p-value in range [0, 1].

    Raises:
        ValueError:
            If required arguments for a given `type` are missing.
    """

    # Filter objects
    names1 = filter_items(obj1, num_col=num_col, cutoff=cutoff, comp_fun=comp_fun)
    names2 = filter_items(obj2, num_col=num_col, cutoff=cutoff, comp_fun=comp_fun)

    # Ensure outputs are lists of strings
    names1 = list(names1)
    names2 = list(names2)

    if type == "2N":
        return pval_sets_2n(names1, names2, universe1)

    if type == "2MN":
        if universe2 is None:
            raise ValueError("`universe2` must be provided when type = '2MN'.")
        return pval_sets_2mn(names1, names2, universe1, universe2)

    if type == "3N":
        if obj3 is None:
            raise ValueError("`obj3` must be provided when type = '3N'.")

        names3 = filter_items(obj3, num_col=num_col, cutoff=cutoff, comp_fun=comp_fun)
        names3 = list(names3)

        return pval_sets_3n(names1, names2, names3, universe1)

    raise ValueError("Unsupported type provided.")
