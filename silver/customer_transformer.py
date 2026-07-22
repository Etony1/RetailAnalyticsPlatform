import pandas as pd

from silver.silver_transformer import (
    read_bronze_table,
    remove_duplicates,
    trim_string_columns,
    write_silver_table,
)


def transform_customers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize the customer dataset.
    """
    df = df.copy()

    df = trim_string_columns(df)
    df = remove_duplicates(df)

    if "email" in df.columns:
        df["email"] = df["email"].str.lower()

    if "state" in df.columns:
        df["state"] = df["state"].str.upper()

    if "customer_id" in df.columns:
        df["customer_id"] = pd.to_numeric(
            df["customer_id"],
            errors="coerce",
        ).astype("Int64")

    date_columns = [
        "date_of_birth",
        "created_date",
        "registration_date",
    ]

    for column in date_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(
                df[column],
                errors="coerce",
            )

    if "customer_id" in df.columns:
        df = df.dropna(subset=["customer_id"])
        df = df.drop_duplicates(subset=["customer_id"], keep="last")

    return df.reset_index(drop=True)


def run_customer_transform() -> pd.DataFrame:
    """
    Read Bronze customers, transform them, and write Silver output.
    """
    bronze_df = read_bronze_table("customers")
    silver_df = transform_customers(bronze_df)
    output_path = write_silver_table(silver_df, "customers")

    print("\nCustomer Silver transformation completed.")
    print(f"Rows read:    {len(bronze_df):,}")
    print(f"Rows written: {len(silver_df):,}")
    print(f"Output:       {output_path}")

    return silver_df


if __name__ == "__main__":
    run_customer_transform()