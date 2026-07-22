from pathlib import Path
from typing import Iterable

import pandas as pd

from config import BRONZE_DATA_DIR, SILVER_DATA_DIR


# ---------------------------------------------------------------------
# Reading & Writing
# ---------------------------------------------------------------------

def read_bronze_table(table_name: str) -> pd.DataFrame:
    """
    Read a Bronze Parquet table.
    """
    file_path = BRONZE_DATA_DIR / f"{table_name}.parquet"

    if not file_path.exists():
        raise FileNotFoundError(file_path)

    return pd.read_parquet(file_path)


def write_silver_table(df: pd.DataFrame, table_name: str) -> Path:
    """
    Write a Silver Parquet table.
    """
    output_path = SILVER_DATA_DIR / f"{table_name}.parquet"

    df.to_parquet(
        output_path,
        index=False,
    )

    return output_path


# ---------------------------------------------------------------------
# Generic Cleaning
# ---------------------------------------------------------------------

def trim_string_columns(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    string_columns = df.select_dtypes(include="object").columns

    for column in string_columns:
        df[column] = df[column].str.strip()

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates()


# ---------------------------------------------------------------------
# Type Conversion
# ---------------------------------------------------------------------

def convert_datetime_columns(
    df: pd.DataFrame,
    columns: Iterable[str],
) -> pd.DataFrame:

    df = df.copy()

    for column in columns:
        if column in df.columns:
            df[column] = pd.to_datetime(
                df[column],
                errors="coerce",
            )

    return df


def convert_integer_columns(
    df: pd.DataFrame,
    columns: Iterable[str],
) -> pd.DataFrame:

    df = df.copy()

    for column in columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            ).astype("Int64")

    return df


def convert_float_columns(
    df: pd.DataFrame,
    columns: Iterable[str],
) -> pd.DataFrame:

    df = df.copy()

    for column in columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            )

    return df


# ---------------------------------------------------------------------
# Validation Helpers
# ---------------------------------------------------------------------

def validate_non_negative(
    df: pd.DataFrame,
    columns: Iterable[str],
) -> pd.DataFrame:

    df = df.copy()

    for column in columns:
        if column in df.columns:
            df = df[df[column] >= 0]

    return df.reset_index(drop=True)


def validate_positive(
    df: pd.DataFrame,
    columns: Iterable[str],
) -> pd.DataFrame:

    df = df.copy()

    for column in columns:
        if column in df.columns:
            df = df[df[column] > 0]

    return df.reset_index(drop=True)