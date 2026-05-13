import pandas as pd

def check_num_col(
    obj: pd.DataFrame | list[str],
    num_col: str,
) -> None:
    """
    Check if num_col is valid input for an object.

    Valid inputs:
    - pandas DataFrame
    - list of character strings

    Args:
        obj:
            A pandas DataFrames with a numeric column or a list of character strings.
        num_col:
            Name of the numeric column.
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


def check_num_col_all(
    objs: list[pd.DataFrame] | list[list[str]],
    num_col: str,
) -> None:
    """
    Check if num_col is valid input for a list of objects.

    Args:
        objs:
            A list containing either:
            - pandas DataFrames with a numeric column, or
            - lists of character strings.
        num_col:
            Name of the numeric column to validate.

    Raises:
        ValueError:
            If any DataFrame fails validation.
    """
    for obj in objs:
        check_num_col(obj, num_col)