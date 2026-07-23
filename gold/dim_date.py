from pathlib import Path

import pandas as pd

from config import GOLD_DATA_DIR
from gold.gold_utils import (read_silver_table,write_gold_table,)

def build_dim_date(start_date="2023-01-01", end_date="2027-12-31"):
    """
    Build a calendar dimension table.
    """

    dates = pd.date_range(start=start_date, end=end_date, freq="D")

    df = pd.DataFrame({"date": dates})

    df["date_key"] = df["date"].dt.strftime("%Y%m%d").astype(int)

    df["year"] = df["date"].dt.year
    df["quarter"] = df["date"].dt.quarter

    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.month_name()

    df["week"] = df["date"].dt.isocalendar().week.astype(int)

    df["day"] = df["date"].dt.day
    df["day_name"] = df["date"].dt.day_name()

    df["day_of_year"] = df["date"].dt.dayofyear

    df["is_weekend"] = df["date"].dt.weekday >= 5

    return df


def write_dim_date(df):
    output_path = GOLD_DATA_DIR / "dim_date.parquet"

    df.to_parquet(output_path, index=False)

    return output_path


def run_dim_date():

    df = build_dim_date()

    output = write_dim_date(df)

    print("\nGold dim_date completed.")

    print(f"Rows written: {len(df):,}")
    print(f"Columns:      {len(df.columns)}")
    print(f"Output:       {output}")

    return df


if __name__ == "__main__":
    run_dim_date()