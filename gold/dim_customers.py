from pathlib import Path

import pandas as pd

from config import GOLD_DATA_DIR, SILVER_DATA_DIR
from gold.gold_utils import (read_silver_table,write_gold_table,)

def read_silver_table(table_name: str) -> pd.DataFrame:
    file_path = SILVER_DATA_DIR / f"{table_name}.parquet"

    if not file_path.exists():
        raise FileNotFoundError(f"Silver table not found: {file_path}")

    return pd.read_parquet(file_path)


def build_dim_customers() -> pd.DataFrame:
    customers = read_silver_table("customers").copy()

    customers = customers.rename(
        columns={
            "customer_id": "customer_key"
        }
    )

    selected_columns = [
        "customer_key",
        "first_name",
        "last_name",
        "email",
        "phone",
        "city",
        "state",
        "zip_code",
        "join_date",
        "loyalty_level",
    ]

    return (
        customers[selected_columns]
        .sort_values("customer_key")
        .reset_index(drop=True)
    )


def write_dim_customers(df: pd.DataFrame) -> Path:
    # output_path = GOLD_DATA_DIR / "dim_customers.parquet"
    # df.to_parquet(output_path, index=False)
    output_path = write_gold_table(df, "dim_customers")
    return output_path


def run_dim_customers():
    df = build_dim_customers()

    output = write_dim_customers(df)

    print("\nGold dim_customers completed.")
    print(f"Rows written: {len(df):,}")
    print(f"Columns:      {len(df.columns)}")
    print(f"Output:       {output}")

    return df


if __name__ == "__main__":
    run_dim_customers()