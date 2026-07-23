from pathlib import Path

import pandas as pd

from config import GOLD_DATA_DIR, SILVER_DATA_DIR
from gold.gold_utils import (read_silver_table,write_gold_table,)

def read_silver_table(table_name: str) -> pd.DataFrame:
    file_path = SILVER_DATA_DIR / f"{table_name}.parquet"

    if not file_path.exists():
        raise FileNotFoundError(f"Silver table not found: {file_path}")

    return pd.read_parquet(file_path)


def build_fact_sales() -> pd.DataFrame:
    """
    Build a line-level sales fact table from Silver orders and order items.
    """
    orders = read_silver_table("orders")
    order_items = read_silver_table("order_items")

    order_columns = [
        "order_id",
        "customer_id",
        "store_id",
        "employee_id",
        "order_date",
        "order_status",
        "payment_method",
        "loyalty_level",
        "discount_rate",
        "discount_amount",
        "tax_amount",
        "shipping_fee",
        "total_amount",
    ]

    fact_sales = order_items.merge(
        orders[order_columns],
        on="order_id",
        how="inner",
        validate="many_to_one",
    )

    fact_sales["gross_sales"] = (
        fact_sales["quantity"] * fact_sales["unit_price"]
    ).round(2)

    fact_sales["cost_amount"] = (
        fact_sales["quantity"] * fact_sales["unit_cost"]
    ).round(2)

    fact_sales["gross_profit"] = (
        fact_sales["gross_sales"] - fact_sales["cost_amount"]
    ).round(2)

    fact_sales["profit_margin"] = (
        fact_sales["gross_profit"]
        / fact_sales["gross_sales"].replace(0, pd.NA)
    ).round(4)

    fact_sales["order_date_key"] = (
        fact_sales["order_date"].dt.strftime("%Y%m%d").astype("Int64")
    )

    selected_columns = [
        "order_item_id",
        "order_id",
        "order_date_key",
        "order_date",
        "customer_id",
        "store_id",
        "employee_id",
        "product_id",
        "quantity",
        "unit_price",
        "unit_cost",
        "gross_sales",
        "cost_amount",
        "gross_profit",
        "profit_margin",
        "line_total",
        "discount_rate",
        "discount_amount",
        "tax_amount",
        "shipping_fee",
        "total_amount",
        "order_status",
        "payment_method",
        "loyalty_level",
    ]

    return (
        fact_sales[selected_columns]
        .sort_values(["order_date", "order_id", "order_item_id"])
        .reset_index(drop=True)
    )


def write_fact_sales(df: pd.DataFrame) -> Path:
    # output_path = GOLD_DATA_DIR / "fact_sales.parquet"
    # df.to_parquet(output_path, index=False)
    output_path = write_gold_table(df, "fact_sales")
    return output_path


def run_fact_sales() -> pd.DataFrame:
    fact_sales = build_fact_sales()
    output_path = write_fact_sales(fact_sales)

    print("\nGold fact_sales completed.")
    print(f"Rows written: {len(fact_sales):,}")
    print(f"Columns:      {len(fact_sales.columns):,}")
    print(f"Output:       {output_path}")

    return fact_sales


if __name__ == "__main__":
    run_fact_sales()