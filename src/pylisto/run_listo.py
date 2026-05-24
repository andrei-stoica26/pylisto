from typing import Any, Dict, List, Literal, Optional
import warnings
import pandas as pd


from .pval_objects import pval_objects
from .multiple_testing import mt_correct_df


def run_listo(
    dict1: Dict[str, Any],
    dict2: Dict[str, Any],
    dict3: Optional[Dict[str, Any]] = None,
    universe1: List[str] = None,
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
    pval_thr: Optional[float] = None,
    n_cores: int = 1,
    verbose: bool = True,
    **kwargs: Any,
) -> pd.DataFrame:
    """
    Assess the overlap of two or three dictionaries of objects.

    This function assesses the overlap of two or three dictionaries of objects
    (character vectors, or data frames having at least one numeric column).

    Args:
        dict1:
            A dictionary containing character vectors or data frames having
            a numeric column. Keys represent group names.
        dict2:
            A dictionary containing character vectors or data frames having
            a numeric column. Keys represent group names.
        dict3:
            Optional third dictionary containing character vectors or data
            frames having a numeric column. Keys represent group names.
        universe1:
            Character vector representing the set from which the items
            corresponding to the elements in `dict1` are selected.
        universe2:
            Optional character vector representing the set from which the items
            corresponding to the elements in `dict2` are selected.
        num_col:
            Name of the numeric column if input objects are data frames.
        is_high_top:
            If True, higher values are considered top-ranked. If False,
            lower values are considered top-ranked.
        max_cutoffs:
            Maximum number of cutoffs to generate for overlap testing.
        mt_method:
            Multiple testing correction method. One of:
            "BY", "holm", "hochberg", "hommel", "bonferroni",
            "BH", "fdr", or "none".
        pval_thr:
            Threshold used to filter results based on adjusted p-values.
            If None, no filtering is performed.
        n_cores:
            Number of cores to use for parallel computation.
        verbose:
            Whether progress messages should be printed.
        **kwargs:
            Additional arguments passed to `mt_correct_df()`.

    Returns:
        A pandas DataFrame listing the p-value and adjusted p-value for each
        overlap. The first columns represent combinations of overlaps, the
        penultimate column contains overlap p-values, and the final column
        contains adjusted overlap p-values.
    """
    if dict3 is None:
        combinations = [
            (name1, name2)
            for name1 in dict1.keys()
            for name2 in dict2.keys()
        ]

        type_: Literal["2N", "2MN", "3N"] = (
            "2N" if universe2 is None else "2MN"
        )

    else:
        combinations = [
            (name1, name2, name3)
            for name1 in dict1.keys()
            for name2 in dict2.keys()
            for name3 in dict3.keys()
        ]

        type_ = "3N"

        if universe2 is not None:
            warnings.warn(
                "Three-way overlaps can currently be computed only for "
                "one universe. `universe2` will be ignored."
            )

    df = pd.DataFrame(combinations)
    df.columns = [f"Group{i}" for i in range(1, len(df.columns) + 1)]

    pvals: List[float] = []

    for _, row in df.iterrows():
        name1 = row["Group1"]
        name2 = row["Group2"]

        obj1 = dict1[name1]
        obj2 = dict2[name2]

        if dict3 is None:
            obj3 = None

            if verbose:
                print(
                    f"Assessing overlap between sets "
                    f"{name1} and {name2}..."
                )

        else:
            name3 = row["Group3"]
            obj3 = dict3[name3]

            if verbose:
                print(
                    f"Assessing overlap between sets "
                    f"{name1}, {name2} and {name3}..."
                )

        pval = pval_objects(
            obj1=obj1,
            obj2=obj2,
            obj3=obj3,
            universe1=universe1,
            universe2=universe2,
            num_col=num_col,
            is_high_top=is_high_top,
            max_cutoffs=max_cutoffs,
            mt_method=mt_method,
            n_cores=n_cores,
            type=type_,
        )

        pvals.append(pval)

    df["pval"] = pvals

    df = mt_correct_df(
        df=df,
        mt_method=mt_method,
        pval_thr=pval_thr,
        **kwargs,
    )

    return df