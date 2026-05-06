import pandas as pd
from typing import Any, List


def check_num_col(obj: Any, num_col: str) -> None:
    """
    Check if num_col is valid input for an object.

    If obj is a pandas DataFrame:
    - Verify that num_col exists as a column
    - Verify that the num_col column is numeric

    Raises
    ------
    ValueError
        If the required column is missing or not numeric.
    """
    if isinstance(obj, pd.DataFrame):
        if num_col not in obj.columns:
            raise ValueError(
                "All data frames must contain a `num_col` column."
            )

        if not pd.api.types.is_numeric_dtype(obj[num_col]):
            raise ValueError(
                "The `num_col` column must be numeric in all data frames."
            )


def check_num_col_all(objs: List[Any], num_col: str) -> None:
    """
    Check if num_col is valid input for a list of objects.

    Parameters
    ----------
    objs : list
        A list containing pandas DataFrames with a numeric column
        or character vectors (e.g., lists of strings).
    num_col : str
        Name of the numeric column to validate.

    Raises
    ------
    ValueError
        If any DataFrame fails validation.
    """
    for obj in objs:
        check_num_col(obj, num_col)