from pathlib import Path

import pandas as pd

from config import GOLD_DATA_DIR, SILVER_DATA_DIR
from gold.gold_utils import (read_silver_table,write_gold_table,)

def read_silver_table(table_name: str) -> pd.DataFrame:
    file_path = SILVER_DATA_DIR / f"{table_name}.parquet"

    if not file_path.exists():
        raise FileNotFoundError(f"Silver table not found: {file_path}")

    return pd.read_parquet(file_path)


def build_dim_products() -> pd.DataFrame:
    products = read_silver_table("products").copy()

    products = products.rename(
        columns={
            "product_id": "product_key"
        }
    )

    selected_columns = [
        "product_key",
        "product_name",
        "category",
        "brand",
        "supplier_id",
        "cost",
        "price",
    ]

    return (
        products[selected_columns]
        .sort_values("product_key")
        .reset_index(drop=True)
    )


def write_dim_products(df: pd.DataFrame) -> Path:
    # output_path = GOLD_DATA_DIR / "dim_products.parquet"
    # df.to_parquet(output_path, index=False)
    output_path = write_gold_table(df, "dim_products")
    return output_path


def run_dim_products():

    df = build_dim_products()

    output = write_dim_products(df)

    print("\nGold dim_products completed.")
    print(f"Rows written: {len(df):,}")
    print(f"Columns:      {len(df.columns)}")
    print(f"Output:       {output}")

    return df


if __name__ == "__main__":
    run_dim_products()