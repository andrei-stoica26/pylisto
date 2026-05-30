from typing import Callable, Iterable, Optional, Literal, Union, List
import pandas as pd
import operator


from .pval_sets import pval_sets_2n, pval_sets_2mn, pval_sets_3n
from .checks import check_num_col_all
from .cutoffs import generate_cutoffs
from .multiple_testing import mt_correct_v


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
    if isinstance(obj, list):
        return obj

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
    overlap_type: Literal["2N", "2MN", "3N"] = "2N",
) -> float:
    """
    Compute the p-value of overlap for two or three objects.

    This function:
    1. Filters input objects using `filter_items`
    2. Converts filtered results into sets of names
    3. Dispatches to the appropriate p-value function depending on `overlap_type`

    Args:
        obj1:
            First input object (list of strings or pandas DataFrame).
        obj2:
            Second input object (list of strings or pandas DataFrame).
        obj3:
            Optional third input object (required when overlap_type = "3N").
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
        overlap_type:
            Type of computation: "2N", "2MN", or "3N".

    Returns:
        p-value in range [0, 1].

    Raises:
        ValueError:
            If required arguments for a given `overlap_type` are missing.
    """

    names1 = filter_items(obj1, num_col=num_col, cutoff=cutoff, comp_fun=comp_fun)
    names2 = filter_items(obj2, num_col=num_col, cutoff=cutoff, comp_fun=comp_fun)

    names1 = list(names1)
    names2 = list(names2)

    if overlap_type == "2N":
        return pval_sets_2n(names1, names2, universe1)

    if overlap_type == "2MN":
        if universe2 is None:
            raise ValueError("`universe2` must be provided when overlap_type = '2MN'.")
        return pval_sets_2mn(names1, names2, universe1, universe2)

    if overlap_type == "3N":
        if obj3 is None:
            raise ValueError("`obj3` must be provided when overlap_type = '3N'.")

        names3 = filter_items(obj3, num_col=num_col, cutoff=cutoff, comp_fun=comp_fun)
        names3 = list(names3)

        return pval_sets_3n(names1, names2, names3, universe1)

    raise ValueError("Unsupported `overlap_type` provided.")


def pval_objects(
    obj1: Union[List[str], pd.DataFrame],
    obj2: Union[List[str], pd.DataFrame],
    universe1: List[str],
    obj3: Optional[Union[List[str], pd.DataFrame]] = None,
    universe2: Optional[List[str]] = None,
    num_col: Optional[str] = None,
    is_high_top: bool = True,
    max_cutoffs: int = 500,
    mt_method: Literal [
        "fdr_by",
        "bonferroni",
        "sidak",
        "holm-sidak",
        "holm",
        "simes-hochberg",
        "hommel",
        "fdr_bh",
        "fdr_tsbh",
        "fdr_tsbky",
    ] = "fdr_by",
    overlap_type: Literal["2N", "2MN", "3N"] = "2N",
) -> float:
    """
    Assess the statistical significance of the overlap of two or three objects.

    This function assesses the statistical significance of the overlap of two
    or three objects (character vectors, or data frames having a numeric column).

    Args:
        obj1:
            First object to compare. Can be a character vector or a data frame
            containing a numeric column.
        obj2:
            Second object to compare. Can be a character vector or a data frame
            containing a numeric column.
        obj3:
            Optional third object for three-set overlap assessment.
        universe1:
            Universe associated with the first object (and second if using the
            same universe).
        universe2:
            Optional second universe when assessing overlap between sets
            belonging to different universes.
        num_col:
            Name of the numeric column if input objects are data frames.
        is_high_top:
            If True, higher values are considered top-ranked (`>` comparison).
            If False, lower values are considered top-ranked (`<` comparison).
        max_cutoffs:
            Maximum number of cutoffs to generate for overlap testing.
        mt_method:
            Multiple testing correction method.
        overlap_type:
            Type of overlap assessment. One of:
            - "2N": two sets belonging to the same universe
            - "2MN": two sets belonging to different universes
            - "3N": three sets belonging to the same universe

    Returns:
        A numeric value in [0, 1] representing the p-value of the overlap
        of the provided objects.
    """
    check_num_col_all([obj1, obj2, obj3], num_col)

    cutoffs = generate_cutoffs(
        obj1=obj1,
        obj2=obj2,
        obj3=obj3,
        num_col=num_col,
        is_high_top=is_high_top,
        max_cutoffs=max_cutoffs,
    )

    comp_fun: Callable[[Any, Any], bool] = (
        operator.gt if is_high_top else operator.lt
    )

    pvals: List[float] = [pval_objects_core(
            obj1=obj1,
            obj2=obj2,
            obj3=obj3,
            universe1=universe1,
            universe2=universe2,
            num_col=num_col,
            cutoff=cutoff,
            comp_fun=comp_fun,
            overlap_type=overlap_type,
        ) for cutoff in cutoffs]

    pval: float = mt_correct_v(
        pvals=pvals,
        mt_method=mt_method,
        mt_stat="median",
    )

    return pval