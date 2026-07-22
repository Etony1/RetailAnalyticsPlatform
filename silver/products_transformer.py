import pandas as pd

from silver.silver_transformer import (
    convert_float_columns,
    convert_integer_columns,
    read_bronze_table,
    remove_duplicates,
    trim_string_columns,
    validate_non_negative,
    write_silver_table,
)


def transform_products(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate the products dataset.
    """
    df = df.copy()

    # Generic cleaning
    df = trim_string_columns(df)
    df = remove_duplicates(df)

    # Type conversions
    df = convert_integer_columns(
        df,
        [
            "product_id",
            "supplier_id",
        ],
    )

    df = convert_float_columns(
        df,
        [
            "cost",
            "price",
        ],
    )

    # Validation
    df = validate_non_negative(
        df,
        [
            "cost",
            "price",
        ],
    )

    # Business rule
    if {"cost", "price"}.issubset(df.columns):
        df = df[df["price"] >= df["cost"]]

    # Standardization
    if "category" in df.columns:
        df["category"] = df["category"].str.title()

    if "brand" in df.columns:
        df["brand"] = df["brand"].str.title()

    return df.reset_index(drop=True)


def run_products_transform():
    bronze_df = read_bronze_table("products")

    silver_df = transform_products(bronze_df)

    output = write_silver_table(
        silver_df,
        "products",
    )

    print("\nProducts Silver transformation completed.")
    print(f"Rows read:    {len(bronze_df):,}")
    print(f"Rows written: {len(silver_df):,}")
    print(f"Output:       {output}")

    return silver_df


if __name__ == "__main__":
    run_products_transform()