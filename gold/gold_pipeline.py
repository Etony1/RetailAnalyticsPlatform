from dataclasses import dataclass

from gold.fact_sales import run_fact_sales
from gold.dim_date import run_dim_date
from gold.dim_customers import run_dim_customers
from gold.dim_products import run_dim_products
from gold.dim_stores import run_dim_stores


@dataclass
class GoldRunResult:
    table_name: str
    row_count: int


def print_summary(results: list[GoldRunResult]) -> None:

    print("\n" + "=" * 80)
    print("GOLD PIPELINE SUMMARY")
    print("=" * 80)

    print(f"{'Table':<25}{'Rows':>12}")

    print("-" * 80)

    total_rows = 0

    for result in results:
        print(f"{result.table_name:<25}{result.row_count:>12,}")
        total_rows += result.row_count

    print("-" * 80)
    print(f"{'TOTAL':<25}{total_rows:>12,}")
    print("=" * 80)

    print(f"\nGold pipeline completed successfully. {len(results)} tables processed.")


def run_gold_pipeline():

    print("\nStarting Gold pipeline...\n")

    results = []

    fact_sales = run_fact_sales()
    results.append(
        GoldRunResult(
            "fact_sales",
            len(fact_sales),
        )
    )

    dim_date = run_dim_date()
    results.append(
        GoldRunResult(
            "dim_date",
            len(dim_date),
        )
    )

    dim_customers = run_dim_customers()
    results.append(
        GoldRunResult(
            "dim_customers",
            len(dim_customers),
        )
    )

    dim_products = run_dim_products()
    results.append(
        GoldRunResult(
            "dim_products",
            len(dim_products),
        )
    )

    dim_stores = run_dim_stores()
    results.append(
        GoldRunResult(
            "dim_stores",
            len(dim_stores),
        )
    )

    print_summary(results)


if __name__ == "__main__":
    run_gold_pipeline()