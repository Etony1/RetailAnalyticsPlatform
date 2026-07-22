from bronze.bronze_loader import load_raw_csv, write_bronze_parquet


def main() -> None:
    customers = load_raw_csv("customers.csv")
    output_path = write_bronze_parquet(customers, "customers")

    print(customers.head())
    print()
    print(f"Rows loaded: {len(customers):,}")
    print(f"Columns: {len(customers.columns)}")
    print(f"Bronze file created: {output_path}")


if __name__ == "__main__":
    main()