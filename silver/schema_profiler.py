from config import BRONZE_DATA_DIR
import pandas as pd


def profile_bronze_tables() -> None:
    """
    Display row counts, column names, data types,
    null counts, and duplicate counts for every Bronze table.
    """
    parquet_files = sorted(BRONZE_DATA_DIR.glob("*.parquet"))

    if not parquet_files:
        raise FileNotFoundError(
            f"No Bronze Parquet files found in {BRONZE_DATA_DIR}"
        )

    for file_path in parquet_files:
        table_name = file_path.stem
        df = pd.read_parquet(file_path)

        print("\n" + "=" * 70)
        print(f"TABLE: {table_name}")
        print("=" * 70)

        print(f"Rows:       {len(df):,}")
        print(f"Columns:    {len(df.columns):,}")
        print(f"Duplicates: {df.duplicated().sum():,}")

        print("\nCOLUMN PROFILE")

        profile = pd.DataFrame(
            {
                "column": df.columns,
                "data_type": [str(df[column].dtype) for column in df.columns],
                "null_count": [
                    int(df[column].isna().sum()) for column in df.columns
                ],
                "unique_count": [
                    int(df[column].nunique(dropna=True))
                    for column in df.columns
                ],
            }
        )

        print(profile.to_string(index=False))


if __name__ == "__main__":
    profile_bronze_tables()