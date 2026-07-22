from __future__ import annotations

from collections.abc import Callable

import pandas as pd


ValidationRule = Callable[[pd.DataFrame], pd.Series]


def valid_price_vs_cost(df: pd.DataFrame) -> pd.Series:
    """
    Product price must be greater than or equal to product cost.
    """
    required = {"price", "cost"}

    if not required.issubset(df.columns):
        return pd.Series(True, index=df.index)

    return df["price"] >= df["cost"]


def valid_order_totals(
    df: pd.DataFrame,
    tolerance: float = 0.01,
) -> pd.Series:
    """
    Validate:

    total_amount =
        subtotal
        - discount_amount
        + tax_amount
        + shipping_fee
    """
    required = {
        "subtotal",
        "discount_amount",
        "tax_amount",
        "shipping_fee",
        "total_amount",
    }

    if not required.issubset(df.columns):
        return pd.Series(True, index=df.index)

    calculated_total = (
        df["subtotal"]
        - df["discount_amount"]
        + df["tax_amount"]
        + df["shipping_fee"]
    )

    difference = (df["total_amount"] - calculated_total).abs()

    return difference <= tolerance


def valid_line_totals(
    df: pd.DataFrame,
    tolerance: float = 0.01,
) -> pd.Series:
    """
    Validate:

    line_total = quantity * unit_price
    """
    required = {
        "quantity",
        "unit_price",
        "line_total",
    }

    if not required.issubset(df.columns):
        return pd.Series(True, index=df.index)

    calculated_total = df["quantity"] * df["unit_price"]
    difference = (df["line_total"] - calculated_total).abs()

    return difference <= tolerance


def valid_discount_rate(df: pd.DataFrame) -> pd.Series:
    """
    Discount rate must be between 0 and 1.
    """
    if "discount_rate" not in df.columns:
        return pd.Series(True, index=df.index)

    return df["discount_rate"].between(0, 1, inclusive="both")


def valid_inventory_levels(df: pd.DataFrame) -> pd.Series:
    """
    Validate basic inventory relationships.
    """
    required = {
        "quantity_on_hand",
        "reorder_point",
        "reorder_quantity",
        "max_stock_level",
    }

    if not required.issubset(df.columns):
        return pd.Series(True, index=df.index)

    return (
        (df["quantity_on_hand"] >= 0)
        & (df["reorder_point"] >= 0)
        & (df["reorder_quantity"] >= 0)
        & (df["max_stock_level"] >= df["reorder_point"])
    )


def valid_supplier_rating(df: pd.DataFrame) -> pd.Series:
    """
    Supplier rating must be between 1 and 5.
    """
    if "rating" not in df.columns:
        return pd.Series(True, index=df.index)

    return df["rating"].between(1, 5, inclusive="both")


def valid_return_quantity(df: pd.DataFrame) -> pd.Series:
    """
    Returned quantity must be greater than zero.
    """
    if "quantity_returned" not in df.columns:
        return pd.Series(True, index=df.index)

    return df["quantity_returned"] > 0


TABLE_VALIDATION_RULES: dict[str, list[ValidationRule]] = {
    "products": [
        valid_price_vs_cost,
    ],
    "orders": [
        valid_order_totals,
        valid_discount_rate,
    ],
    "order_items": [
        valid_line_totals,
    ],
    "inventory_snapshot": [
        valid_inventory_levels,
    ],
    "returns": [
        valid_return_quantity,
    ],
    "suppliers": [
        valid_supplier_rating,
    ],
}


def apply_validation_rules(
    df: pd.DataFrame,
    table_name: str,
) -> tuple[pd.DataFrame, int]:
    """
    Apply all configured business validation rules for a table.

    Returns:
        Tuple containing:
        - valid records
        - invalid record count
    """
    rules = TABLE_VALIDATION_RULES.get(table_name, [])

    if not rules:
        return df.reset_index(drop=True), 0

    valid_mask = pd.Series(True, index=df.index)

    for rule in rules:
        rule_result = rule(df).fillna(False)
        valid_mask &= rule_result

    valid_df = df.loc[valid_mask].copy()
    invalid_count = int((~valid_mask).sum())

    return valid_df.reset_index(drop=True), invalid_count