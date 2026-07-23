from pathlib import Path

import pandas as pd

from config import GOLD_DATA_DIR, SILVER_DATA_DIR


def read_silver_table(table_name: str) -> pd.DataFrame:
    """Read a Silver table from Parquet."""
    file_path = SILVER_DATA_DIR / f"{table_name}.parquet"

    if not file_path.exists():
        raise FileNotFoundError(f"Silver table not found: {file_path}")

    return pd.read_parquet(file_path)


def write_gold_table(df: pd.DataFrame, table_name: str) -> Path:
    """Write a Gold table to Parquet."""
    output_path = GOLD_DATA_DIR / f"{table_name}.parquet"

    df.to_parquet(output_path, index=False)

    return output_path