from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from silver.business_rules import apply_business_rules
from silver.silver_transformer import (
    convert_datetime_columns,
    convert_float_columns,
    convert_integer_columns,
    read_bronze_table,
    remove_duplicates,
    trim_string_columns,
    validate_non_negative,
    validate_positive,
    write_silver_table,
)
from silver.table_config import TABLE_CONFIG
from silver.validation_rules import apply_validation_rules


@dataclass
class TableRunResult:
    table_name: str
    rows_read: int
    rows_after_generic_cleaning: int
    invalid_rows: int
    rows_written: int
    output_path: str


def apply_generic_transformations(
    df: pd.DataFrame,
    config: dict,
) -> pd.DataFrame:
    """
    Apply reusable Silver transformations from table configuration.
    """
    df = trim_string_columns(df)
    df = remove_duplicates(df)

    df = convert_datetime_columns(
        df,
        config.get("datetime", []),
    )

    df = convert_integer_columns(
        df,
        config.get("integers", []),
    )

    df = convert_float_columns(
        df,
        config.get("floats", []),
    )

    df = validate_non_negative(
        df,
        config.get("non_negative", []),
    )

    df = validate_positive(
        df,
        config.get("positive", []),
    )

    return df.reset_index(drop=True)


def run_table_transform(table_name: str) -> TableRunResult:
    """
    Process one Bronze table into Silver.
    """
    if table_name not in TABLE_CONFIG:
        raise KeyError(f"No Silver configuration found for: {table_name}")

    bronze_df = read_bronze_table(table_name)
    rows_read = len(bronze_df)

    silver_df = apply_generic_transformations(
        bronze_df,
        TABLE_CONFIG[table_name],
    )

    silver_df = apply_business_rules(
        silver_df,
        table_name,
    )

    rows_after_generic_cleaning = len(silver_df)

    silver_df, invalid_rows = apply_validation_rules(
        silver_df,
        table_name,
    )

    output_path = write_silver_table(
        silver_df,
        table_name,
    )

    return TableRunResult(
        table_name=table_name,
        rows_read=rows_read,
        rows_after_generic_cleaning=rows_after_generic_cleaning,
        invalid_rows=invalid_rows,
        rows_written=len(silver_df),
        output_path=str(output_path),
    )


def print_run_summary(results: list[TableRunResult]) -> None:
    """
    Print a summary of the Silver pipeline run.
    """
    print("\n" + "=" * 84)
    print("SILVER PIPELINE SUMMARY")
    print("=" * 84)

    print(
        f"{'Table':<26}"
        f"{'Read':>10}"
        f"{'After Clean':>14}"
        f"{'Invalid':>10}"
        f"{'Written':>12}"
    )

    print("-" * 84)

    for result in results:
        print(
            f"{result.table_name:<26}"
            f"{result.rows_read:>10,}"
            f"{result.rows_after_generic_cleaning:>14,}"
            f"{result.invalid_rows:>10,}"
            f"{result.rows_written:>12,}"
        )

    print("-" * 84)

    print(
        f"{'TOTAL':<26}"
        f"{sum(item.rows_read for item in results):>10,}"
        f"{sum(item.rows_after_generic_cleaning for item in results):>14,}"
        f"{sum(item.invalid_rows for item in results):>10,}"
        f"{sum(item.rows_written for item in results):>12,}"
    )

    print("=" * 84)


def run_silver_pipeline() -> list[TableRunResult]:
    """
    Process all configured Bronze tables into Silver.
    """
    results: list[TableRunResult] = []

    print("\nStarting Silver pipeline...\n")

    for table_name in TABLE_CONFIG:
        try:
            result = run_table_transform(table_name)
            results.append(result)

            print(
                f"[SUCCESS] {table_name:<24} "
                f"read={result.rows_read:>7,}  "
                f"written={result.rows_written:>7,}  "
                f"invalid={result.invalid_rows:>5,}"
            )

        except Exception as exc:
            print(f"[FAILED]  {table_name:<24} error={exc}")
            raise

    print_run_summary(results)

    print(
        f"\nSilver pipeline completed successfully. "
        f"{len(results)} tables processed."
    )

    return results


if __name__ == "__main__":
    run_silver_pipeline()