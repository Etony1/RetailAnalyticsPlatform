from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

import pandas as pd


@dataclass
class ValidationResult:
    rule: str
    status: str
    severity: str
    records: int
    message: str
    examples: list[Any]


class DataQuality:
    """
    Collects validation results and produces a consolidated
    data-quality report.
    """

    VALID_STATUSES = {"PASS", "FAIL", "WARNING"}
    VALID_SEVERITIES = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}

    def __init__(self) -> None:
        self.results: list[ValidationResult] = []

    def add_result(
        self,
        rule: str,
        
        status: str,
        severity: str,
        records: int,
        message: str,
        examples: list[Any] | None = None,
    ) -> None:
        """
        Add one validation result to the report.
        """

        status = status.upper()
        severity = severity.upper()

        if status not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid status '{status}'. "
                f"Use one of: {sorted(self.VALID_STATUSES)}"
            )

        if severity not in self.VALID_SEVERITIES:
            raise ValueError(
                f"Invalid severity '{severity}'. "
                f"Use one of: {sorted(self.VALID_SEVERITIES)}"
            )

        if records < 0:
            raise ValueError("records cannot be negative.")

        self.results.append(
            ValidationResult(
                rule=rule,
                status=status,
                severity=severity,
                records=records,
                message=message,
                examples=examples or [],
            )
        )

    def has_critical_failures(self) -> bool:
        """
        Return True when at least one critical validation has failed.
        """

        return any(
            result.status == "FAIL"
            and result.severity == "CRITICAL"
            for result in self.results
        )

    def get_summary(self) -> dict[str, int | float | str]:
        """
        Return summary statistics for all validation checks.
        """

        total_checks = len(self.results)
        passed = sum(result.status == "PASS" for result in self.results)
        failed = sum(result.status == "FAIL" for result in self.results)
        warnings = sum(result.status == "WARNING" for result in self.results)

        score = (
            round((passed / total_checks) * 100, 2)
            if total_checks > 0
            else 0.0
        )

        overall_status = (
            "FAILED"
            if self.has_critical_failures()
            else "PASSED WITH WARNINGS"
            if warnings > 0 or failed > 0
            else "PASSED"
        )

        return {
            "total_checks": total_checks,
            "passed": passed,
            "failed": failed,
            "warnings": warnings,
            "score": score,
            "overall_status": overall_status,
        }

    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert validation results into a pandas DataFrame.
        """

        return pd.DataFrame(
            [asdict(result) for result in self.results]
        )

    def save_report(self, output_path: str) -> None:
        """
        Save the detailed validation report as a CSV file.
        """

        report_df = self.to_dataframe()
        report_df.to_csv(output_path, index=False)

    def report(self) -> None:
        """
        Print a readable validation report to the terminal.
        """

        print("\n" + "=" * 70)
        print("Retail Analytics Data Quality Report")
        print("=" * 70)

        if not self.results:
            print("No validation checks were run.")
            print("=" * 70)
            return

        for result in self.results:
            print(
                f"[{result.status}] "
                f"{result.rule} "
                f"({result.severity})"
            )
            print(f"Records affected: {result.records}")
            print(result.message)

            if result.examples:
                print("Examples:")
                for example in result.examples:
                    print(f"   • {example}")

            print("-" * 70)

        summary = self.get_summary()

        print("SUMMARY")
        print("-" * 70)
        print(f"Checks run:        {summary['total_checks']}")
        print(f"Passed:            {summary['passed']}")
        print(f"Failed:            {summary['failed']}")
        print(f"Warnings:          {summary['warnings']}")
        print(f"Quality score:     {summary['score']}%")
        print(f"Overall status:    {summary['overall_status']}")
        print("=" * 70)

# if __name__ == "__main__":
#     dq = DataQuality()

#     dq.add_result(
#         rule="Unique Customer IDs",
#         status="PASS",
#         severity="CRITICAL",
#         records=0,
#         message="All customer IDs are unique."
#     )

#     dq.add_result(
#         rule="Unique Customer Emails",
#         status="FAIL",
#         severity="CRITICAL",
#         records=2,
#         message="Duplicate customer emails were found.",
#         examples=["test@example.com", "sample@example.com"]
#     )

#     dq.report()