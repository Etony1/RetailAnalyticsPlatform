from pathlib import Path

import pandas as pd

from config import GOLD_DATA_DIR, SILVER_DATA_DIR
from gold.gold_utils import (read_silver_table,write_gold_table,)

def read_silver_table(table_name: str) -> pd.DataFrame:
    file_path = SILVER_DATA_DIR / f"{table_name}.parquet"

    if not file_path.exists():
        raise FileNotFoundError(f"Silver table not found: {file_path}")

    return pd.read_parquet(file_path)


def build_dim_stores() -> pd.DataFrame:
    stores = read_silver_table("stores").copy()

    stores = stores.rename(
        columns={
            "store_id": "store_key",
        }
    )

    selected_columns = [
        "store_key",
        "store_name",
        "city",
        "state",
        "region",
    ]

    return (
        stores[selected_columns]
        .sort_values("store_key")
        .reset_index(drop=True)
    )


def write_dim_stores(df: pd.DataFrame) -> Path:
    # output_path = GOLD_DATA_DIR / "dim_stores.parquet"
    # df.to_parquet(output_path, index=False)
    output_path = write_gold_table(df, "dim_stores")
    return output_path


def run_dim_stores() -> pd.DataFrame:
    df = build_dim_stores()
    output_path = write_dim_stores(df)

    print("\nGold dim_stores completed.")
    print(f"Rows written: {len(df):,}")
    print(f"Columns:      {len(df.columns)}")
    print(f"Output:       {output_path}")

    return df


if __name__ == "__main__":
    run_dim_stores()