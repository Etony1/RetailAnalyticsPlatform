from pathlib import Path

from bronze.bronze_loader import load_raw_csv, write_bronze_parquet


BRONZE_TABLES = {
    "customers": "customers.csv",
    "employees": "employees.csv",
    "inventory_snapshot": "inventory_snapshot.csv",
    "inventory_transactions": "inventory_transactions.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "products": "products.csv",
    "returns": "returns.csv",
    "stores": "stores.csv",
    "suppliers": "suppliers.csv",
}


def run_bronze_pipeline() -> list[Path]:
    """Load all approved raw CSV files and write Bronze Parquet datasets."""
    written_files: list[Path] = []

    print("\nStarting Bronze ingestion pipeline...\n")

    for table_name, file_name in BRONZE_TABLES.items():
        try:
            dataframe = load_raw_csv(file_name)
            output_path = write_bronze_parquet(dataframe, table_name)
            written_files.append(output_path)

            print(
                f"[SUCCESS] {table_name:<24} "
                f"rows={len(dataframe):>6,}  "
                f"output={output_path.name}"
            )

        except Exception as exc:
            print(f"[FAILED]  {table_name:<24} error={exc}")
            raise

    print(
        f"\nBronze pipeline completed successfully. "
        f"{len(written_files)} tables written."
    )

    return written_files


if __name__ == "__main__":
    run_bronze_pipeline()