"""
return_validation.py

Validates customer returns for referential integrity, valid quantities,
refund amounts, return reasons, and consistency with original orders.
"""

from __future__ import annotations

import pandas as pd

from validations.data_quality import DataQuality


TOLERANCE = 0.01

# VALID_RETURN_REASONS = {
#     "damaged",
#     "defective",
#     "wrong item",
#     "changed mind",
#     "not as described",
#     "other",
# }
VALID_RETURN_REASONS = {
    "damaged",
    "defective",
    "wrong item",
    "wrong size",
    "customer changed mind",
    "changed mind",
    "late delivery",
    "not as described",
    "other",
}

def validate_unique_return_ids(
    returns: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate that return IDs are unique."""

    duplicate_rows = returns[
        returns["return_id"].duplicated(keep=False)
    ].sort_values("return_id")

    dq.add_result(
        rule="Unique Return IDs",
        status="PASS" if duplicate_rows.empty else "FAIL",
        severity="CRITICAL",
        records=len(duplicate_rows),
        message=(
            "All return IDs are unique."
            if duplicate_rows.empty
            else f"{len(duplicate_rows)} rows contain duplicate return IDs."
        ),
        examples=duplicate_rows.head(5).to_dict("records"),
    )


def validate_return_order_fk(
    returns: pd.DataFrame,
    orders: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate return order IDs."""

    invalid_rows = returns[
        ~returns["source_order_id"].isin(orders["order_id"])
    ]

    dq.add_result(
        rule="Valid Return Order IDs",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="CRITICAL",
        records=len(invalid_rows),
        message=(
            "All returned orders exist in the orders table."
            if invalid_rows.empty
            else f"{len(invalid_rows)} returns reference invalid orders."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )

def validate_return_order_item_fk(
    returns: pd.DataFrame,
    order_items: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate return order-item IDs."""

    invalid_rows = returns[
        ~returns["order_item_id"].isin(order_items["order_item_id"])
    ]

    dq.add_result(
        rule="Valid Return Order Item IDs",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="CRITICAL",
        records=len(invalid_rows),
        message=(
            "All return order-item IDs are valid."
            if invalid_rows.empty
            else (
                f"{len(invalid_rows)} returns reference "
                "invalid order items."
            )
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )






def validate_return_product_fk(
    returns: pd.DataFrame,
    products: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate return product IDs."""

    invalid_rows = returns[
        ~returns["product_id"].isin(products["product_id"])
    ]

    dq.add_result(
        rule="Valid Return Product IDs",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="CRITICAL",
        records=len(invalid_rows),
        message=(
            "All returned products exist in the products table."
            if invalid_rows.empty
            else f"{len(invalid_rows)} returns reference invalid products."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_return_quantities(
    returns: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate that returned quantities are positive."""

    invalid_rows = returns[
        returns["quantity_returned"].isna()
        | (returns["quantity_returned"] <= 0)
    ]

    dq.add_result(
        rule="Positive Return Quantities",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="HIGH",
        records=len(invalid_rows),
        message=(
            "All returned quantities are positive."
            if invalid_rows.empty
            else (
                f"{len(invalid_rows)} returns contain "
                "invalid returned quantities."
            )
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_return_reasons(
    returns: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate return reasons against approved values."""

    normalized_reasons = (
        returns["return_reason"]
        .astype("string")
        .str.lower()
        .str.strip()
    )

    invalid_rows = returns[
        normalized_reasons.isna()
        | ~normalized_reasons.isin(VALID_RETURN_REASONS)
    ]

    dq.add_result(
        rule="Valid Return Reasons",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="MEDIUM",
        records=len(invalid_rows),
        message=(
            "All return reasons are valid."
            if invalid_rows.empty
            else f"{len(invalid_rows)} returns contain invalid reasons."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_refund_amounts(
    returns: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate that refund amounts are zero or greater."""

    invalid_rows = returns[
        returns["refund_amount"].isna()
        | (returns["refund_amount"] < 0)
    ]

    dq.add_result(
        rule="Non-Negative Refund Amounts",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="HIGH",
        records=len(invalid_rows),
        message=(
            "All refund amounts are valid."
            if invalid_rows.empty
            else f"{len(invalid_rows)} returns have invalid refund amounts."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_return_dates(
    returns: pd.DataFrame,
    orders: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate that return dates are not before their original order dates."""

    comparison = returns[
        ["return_id", "source_order_id", "return_date"]
    ].merge(
        orders[["order_id", "order_date"]],
        on="source_order_id",
        how="left",
    )

    comparison["return_date"] = pd.to_datetime(
        comparison["return_date"],
        errors="coerce",
    )

    comparison["order_date"] = pd.to_datetime(
        comparison["order_date"],
        errors="coerce",
    )

    invalid_rows = comparison[
        comparison["return_date"].isna()
        | comparison["order_date"].isna()
        | (comparison["return_date"] < comparison["order_date"])
    ]

    dq.add_result(
        rule="Valid Return Dates",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="HIGH",
        records=len(invalid_rows),
        message=(
            "All return dates occur on or after their order dates."
            if invalid_rows.empty
            else f"{len(invalid_rows)} returns contain invalid dates."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_return_items_belong_to_orders(
    returns: pd.DataFrame,
    order_items: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate that each returned product was included in its original order."""

    valid_items = order_items[
        ["order_id", "product_id"]
    ].drop_duplicates()

    comparison = returns.merge(
        valid_items.assign(item_exists=True),
        on=["order_id", "product_id"],
        how="left",
    )

    invalid_rows = comparison[
        comparison["item_exists"].isna()
    ]

    dq.add_result(
        rule="Returned Products Belong to Original Orders",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="CRITICAL",
        records=len(invalid_rows),
        message=(
            "All returned products belong to their original orders."
            if invalid_rows.empty
            else (
                f"{len(invalid_rows)} returns reference products "
                "not purchased in the original order."
            )
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_return_quantity_not_exceeded(
    returns: pd.DataFrame,
    order_items: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate that cumulative returned quantity does not exceed purchased quantity."""

    returned = (
        returns.groupby(
            "order_item_id",
            as_index=False,
        )["quantity_returned"]
        .sum()
        .rename(
            columns={
                "quantity_returned": "total_quantity_returned"
            }
        )
    )

    purchased = order_items[
        ["order_item_id", "quantity"]
    ].rename(
        columns={"quantity": "purchased_quantity"}
    )

    comparison = returned.merge(
        purchased,
        on="order_item_id",
        how="left",
    )

    invalid_rows = comparison[
        comparison["purchased_quantity"].isna()
        | (
            comparison["total_quantity_returned"]
            > comparison["purchased_quantity"]
        )
    ]

    dq.add_result(
        rule="Returned Quantity Does Not Exceed Purchased Quantity",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="CRITICAL",
        records=len(invalid_rows),
        message=(
            "All returned quantities are within purchased quantities."
            if invalid_rows.empty
            else (
                f"{len(invalid_rows)} order items have returned "
                "quantities greater than purchased quantities."
            )
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )

def validate_return_order_item_consistency(
    returns: pd.DataFrame,
    order_items: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate that each order item belongs to the return's source order."""

    reference = order_items[
        ["order_item_id", "order_id", "product_id", "quantity"]
    ].rename(
        columns={
            "order_id": "expected_order_id",
            "product_id": "expected_product_id",
            "quantity": "purchased_quantity",
        }
    )

    comparison = returns.merge(
        reference,
        on="order_item_id",
        how="left",
    )

    invalid_rows = comparison[
        comparison["expected_order_id"].isna()
        | (
            comparison["source_order_id"]
            != comparison["expected_order_id"]
        )
    ]

    dq.add_result(
        rule="Return Order Item Matches Source Order",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="CRITICAL",
        records=len(invalid_rows),
        message=(
            "All returned order items belong to their source orders."
            if invalid_rows.empty
            else (
                f"{len(invalid_rows)} returns contain order items "
                "that do not match their source orders."
            )
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )

def validate_return_product_consistency(
    returns: pd.DataFrame,
    order_items: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate that returned product matches the original order item."""

    reference = order_items[
        ["order_item_id", "product_id"]
    ].rename(
        columns={"product_id": "expected_product_id"}
    )

    comparison = returns.merge(
        reference,
        on="order_item_id",
        how="left",
    )

    invalid_rows = comparison[
        comparison["expected_product_id"].isna()
        | (
            comparison["product_id"]
            != comparison["expected_product_id"]
        )
    ]

    dq.add_result(
        rule="Returned Product Matches Order Item",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="CRITICAL",
        records=len(invalid_rows),
        message=(
            "All returned products match their original order items."
            if invalid_rows.empty
            else (
                f"{len(invalid_rows)} returns contain products "
                "that do not match their order items."
            )
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )

def validate_return_dates(
    returns: pd.DataFrame,
    orders: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate that return dates are not before order dates."""

    comparison = returns[
        ["return_id", "source_order_id", "return_date"]
    ].merge(
        orders[["order_id", "order_date"]],
        left_on="source_order_id",
        right_on="order_id",
        how="left",
    )

    comparison["return_date"] = pd.to_datetime(
        comparison["return_date"],
        errors="coerce",
    )

    comparison["order_date"] = pd.to_datetime(
        comparison["order_date"],
        errors="coerce",
    )

    invalid_rows = comparison[
        comparison["return_date"].isna()
        | comparison["order_date"].isna()
        | (
            comparison["return_date"]
            < comparison["order_date"]
        )
    ]

    dq.add_result(
        rule="Valid Return Dates",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="HIGH",
        records=len(invalid_rows),
        message=(
            "All return dates occur on or after their order dates."
            if invalid_rows.empty
            else f"{len(invalid_rows)} returns contain invalid dates."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_returns(
    returns: pd.DataFrame,
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    products: pd.DataFrame,
    dq: DataQuality,
) -> None:
    validate_unique_return_ids(returns, dq)
    validate_return_order_fk(returns, orders, dq)
    validate_return_order_item_fk(returns, order_items, dq)
    validate_return_product_fk(returns, products, dq)
    validate_return_quantities(returns, dq)
    validate_return_reasons(returns, dq)
    validate_refund_amounts(returns, dq)
    validate_return_dates(returns, orders, dq)
    validate_return_order_item_consistency(returns,order_items,dq,)
    validate_return_product_consistency(returns,order_items,dq,)
    validate_return_quantity_not_exceeded(returns,order_items,dq,)