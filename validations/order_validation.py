"""
order_validation.py

Business purpose:
Validates order data for referential integrity, valid business values,
and consistency between orders and their associated order items.
"""

from __future__ import annotations

import pandas as pd

from validations.data_quality import DataQuality


TOLERANCE = 0.01

# VALID_PAYMENT_METHODS = {
#     "Cash",
#     "Credit Card",
#     "Debit Card",
#     "Gift Card",
#     "Online",
# }
VALID_PAYMENT_METHODS = {
    "cash",
    "credit card",
    "debit card",
    "gift card",
    "online",
    "Cash",
    "Credit Card",
    "Debit Card",
    "Gift Card",
    "Online",
    "Mobile Payment",
    "mobile payment",
}
VALID_ORDER_STATUSES = {
    "Pending",
    "Completed",
    "Cancelled",
    "Returned",
}

VALID_LOYALTY_LEVELS = {
    "Bronze",
    "Silver",
    "Gold",
    "Platinum",
}


def validate_customer_fk(
    orders: pd.DataFrame,
    customers: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate that every order customer_id exists in customers."""

    invalid_rows = orders[
        ~orders["customer_id"].isin(customers["customer_id"])
    ]

    dq.add_result(
        rule="Valid Order Customer IDs",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="CRITICAL",
        records=len(invalid_rows),
        message=(
            "All order customer IDs exist in the customer table."
            if invalid_rows.empty
            else f"{len(invalid_rows)} orders contain invalid customer IDs."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_store_fk(
    orders: pd.DataFrame,
    stores: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate that every order store_id exists in stores."""

    invalid_rows = orders[
        ~orders["store_id"].isin(stores["store_id"])
    ]

    dq.add_result(
        rule="Valid Order Store IDs",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="CRITICAL",
        records=len(invalid_rows),
        message=(
            "All order store IDs exist in the store table."
            if invalid_rows.empty
            else f"{len(invalid_rows)} orders contain invalid store IDs."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_employee_fk(
    orders: pd.DataFrame,
    employees: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate that every order employee_id exists in employees."""

    invalid_rows = orders[
        ~orders["employee_id"].isin(employees["employee_id"])
    ]

    dq.add_result(
        rule="Valid Order Employee IDs",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="CRITICAL",
        records=len(invalid_rows),
        message=(
            "All order employee IDs exist in the employee table."
            if invalid_rows.empty
            else f"{len(invalid_rows)} orders contain invalid employee IDs."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_unique_order_ids(
    orders: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate that order_id is unique."""

    duplicate_rows = orders[
        orders["order_id"].duplicated(keep=False)
    ].sort_values("order_id")

    dq.add_result(
        rule="Unique Order IDs",
        status="PASS" if duplicate_rows.empty else "FAIL",
        severity="CRITICAL",
        records=len(duplicate_rows),
        message=(
            "All order IDs are unique."
            if duplicate_rows.empty
            else f"{len(duplicate_rows)} rows contain duplicate order IDs."
        ),
        examples=duplicate_rows.head(5).to_dict("records"),
    )


def validate_non_negative_financial_values(
    orders: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate that financial fields do not contain negative values."""

    financial_columns = [
        "shipping_fee",
        "tax_amount",
        "discount_amount",
        "subtotal",
        "total_amount",
    ]

    available_columns = [
        column for column in financial_columns if column in orders.columns
    ]

    invalid_mask = (
        orders[available_columns].lt(0).any(axis=1)
        if available_columns
        else pd.Series(False, index=orders.index)
    )

    invalid_rows = orders.loc[
        invalid_mask,
        ["order_id", *available_columns],
    ]

    dq.add_result(
        rule="Non-Negative Order Financial Values",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="HIGH",
        records=len(invalid_rows),
        message=(
            "All order financial values are non-negative."
            if invalid_rows.empty
            else f"{len(invalid_rows)} orders contain negative financial values."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )



def validate_discount_rate(
    orders: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate that discount_rate is between 0 and 1."""

    invalid_rows = orders[
        orders["discount_rate"].isna()
        | ~orders["discount_rate"].between(0, 1)
    ][["order_id", "discount_rate"]]

    dq.add_result(
        rule="Valid Order Discount Rates",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="HIGH",
        records=len(invalid_rows),
        message=(
            "All discount rates are between 0 and 1."
            if invalid_rows.empty
            else f"{len(invalid_rows)} orders contain invalid discount rates."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_payment_methods(
    orders: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate payment methods against approved business values."""

    invalid_rows = orders[
        orders["payment_method"].isna()
        | ~orders["payment_method"].isin(VALID_PAYMENT_METHODS)
    ][["order_id", "payment_method"]]

    dq.add_result(
        rule="Valid Payment Methods",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="MEDIUM",
        records=len(invalid_rows),
        message=(
            "All payment methods are valid."
            if invalid_rows.empty
            else f"{len(invalid_rows)} orders contain invalid payment methods."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_order_statuses(
    orders: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate order statuses against approved business values."""

    invalid_rows = orders[
        orders["order_status"].isna()
        | ~orders["order_status"].isin(VALID_ORDER_STATUSES)
    ][["order_id", "order_status"]]

    dq.add_result(
        rule="Valid Order Statuses",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="MEDIUM",
        records=len(invalid_rows),
        message=(
            "All order statuses are valid."
            if invalid_rows.empty
            else f"{len(invalid_rows)} orders contain invalid statuses."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_loyalty_levels(
    orders: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate loyalty levels stored on orders."""

    invalid_rows = orders[
        orders["loyalty_level"].isna()
        | ~orders["loyalty_level"].isin(VALID_LOYALTY_LEVELS)
    ][["order_id", "loyalty_level"]]

    dq.add_result(
        rule="Valid Order Loyalty Levels",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="MEDIUM",
        records=len(invalid_rows),
        message=(
            "All order loyalty levels are valid."
            if invalid_rows.empty
            else f"{len(invalid_rows)} orders contain invalid loyalty levels."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_order_subtotals(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """
    Validate that order subtotal equals the sum of its order-item line totals.

    Supports either:
    - an existing line_total column, or
    - quantity multiplied by unit_price.
    """

    items = order_items.copy()

    if "line_total" not in items.columns:
        required_columns = {"quantity", "unit_price"}

        if not required_columns.issubset(items.columns):
            raise ValueError(
                "order_items must contain line_total or both quantity and unit_price."
            )

        items["line_total"] = items["quantity"] * items["unit_price"]

    calculated_subtotals = (
        items.groupby("order_id", as_index=False)["line_total"]
        .sum()
        .rename(columns={"line_total": "expected_subtotal"})
    )

    comparison = orders[
        ["order_id", "subtotal"]
    ].merge(
        calculated_subtotals,
        on="order_id",
        how="left",
    )

    comparison["expected_subtotal"] = comparison[
        "expected_subtotal"
    ].fillna(0)

    comparison["subtotal_difference"] = (
        comparison["subtotal"] - comparison["expected_subtotal"]
    ).abs()

    invalid_rows = comparison[
        comparison["subtotal"].isna()
        | (comparison["subtotal_difference"] > TOLERANCE)
    ]

    dq.add_result(
        rule="Order Subtotals Match Order Items",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="CRITICAL",
        records=len(invalid_rows),
        message=(
            "All order subtotals match their order-item totals."
            if invalid_rows.empty
            else f"{len(invalid_rows)} orders have incorrect subtotals."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_discount_amounts(
    orders: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate discount_amount using subtotal multiplied by discount_rate."""

    comparison = orders[
        [
            "order_id",
            "subtotal",
            "discount_rate",
            "discount_amount",
        ]
    ].copy()

    comparison["expected_discount"] = (
        comparison["subtotal"] * comparison["discount_rate"]
    ).round(2)

    comparison["discount_difference"] = (
        comparison["discount_amount"]
        - comparison["expected_discount"]
    ).abs()

    invalid_rows = comparison[
        comparison[
            ["subtotal", "discount_rate", "discount_amount"]
        ].isna().any(axis=1)
        | (comparison["discount_difference"] > TOLERANCE)
    ]

    dq.add_result(
        rule="Correct Order Discount Amounts",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="HIGH",
        records=len(invalid_rows),
        message=(
            "All order discount amounts are correct."
            if invalid_rows.empty
            else f"{len(invalid_rows)} orders have incorrect discount amounts."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_total_amounts(
    orders: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """
    Validate total amount using:

    subtotal + tax_amount + shipping_fee - discount_amount
    """

    comparison = orders[
        [
            "order_id",
            "subtotal",
            "tax_amount",
            "shipping_fee",
            "discount_amount",
            "total_amount",
        ]
    ].copy()

    comparison["expected_total"] = (
        comparison["subtotal"]
        + comparison["tax_amount"]
        + comparison["shipping_fee"]
        - comparison["discount_amount"]
    ).round(2)

    comparison["total_difference"] = (
        comparison["total_amount"]
        - comparison["expected_total"]
    ).abs()

    invalid_rows = comparison[
        comparison[
            [
                "subtotal",
                "tax_amount",
                "shipping_fee",
                "discount_amount",
                "total_amount",
            ]
        ].isna().any(axis=1)
        | (comparison["total_difference"] > TOLERANCE)
    ]

    dq.add_result(
        rule="Correct Order Total Amounts",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="CRITICAL",
        records=len(invalid_rows),
        message=(
            "All order totals are correct."
            if invalid_rows.empty
            else f"{len(invalid_rows)} orders have incorrect total amounts."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_orders(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    customers: pd.DataFrame,
    stores: pd.DataFrame,
    employees: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Run the complete order validation suite."""

    validate_unique_order_ids(orders, dq)

    validate_customer_fk(
        orders=orders,
        customers=customers,
        dq=dq,
    )

    validate_store_fk(
        orders=orders,
        stores=stores,
        dq=dq,
    )

    validate_employee_fk(
        orders=orders,
        employees=employees,
        dq=dq,
    )

    validate_non_negative_financial_values(orders, dq)
    validate_discount_rate(orders, dq)
    validate_payment_methods(orders, dq)
    validate_order_statuses(orders, dq)
    validate_loyalty_levels(orders, dq)

    validate_order_subtotals(
        orders=orders,
        order_items=order_items,
        dq=dq,
    )

    validate_discount_amounts(orders, dq)
    validate_total_amounts(orders, dq)