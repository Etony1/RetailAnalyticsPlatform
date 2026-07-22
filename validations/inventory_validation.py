"""
inventory_validation.py

Validates inventory snapshots and inventory transactions for uniqueness,
referential integrity, quantity accuracy, and valid business values.
"""

from __future__ import annotations

import pandas as pd

from validations.data_quality import DataQuality


VALID_TRANSACTION_TYPES = {
    "sale",
    "return",
    "restock",
    "adjustment",
    "transfer_in",
    "transfer_out",
}


def validate_inventory_composite_key(
    inventory: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate that store_id and product_id form a unique inventory key."""

    duplicate_rows = inventory[
        inventory.duplicated(
            subset=["store_id", "product_id"],
            keep=False,
        )
    ].sort_values(["store_id", "product_id"])

    dq.add_result(
        rule="Unique Inventory Store-Product Records",
        status="PASS" if duplicate_rows.empty else "FAIL",
        severity="CRITICAL",
        records=len(duplicate_rows),
        message=(
            "Each store-product combination appears once in inventory."
            if duplicate_rows.empty
            else (
                f"{len(duplicate_rows)} inventory rows contain duplicate "
                "store-product combinations."
            )
        ),
        examples=duplicate_rows.head(5).to_dict("records"),
    )


def validate_inventory_store_fk(
    inventory: pd.DataFrame,
    stores: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate inventory store IDs against the stores table."""

    invalid_rows = inventory[
        ~inventory["store_id"].isin(stores["store_id"])
    ]

    dq.add_result(
        rule="Valid Inventory Store IDs",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="CRITICAL",
        records=len(invalid_rows),
        message=(
            "All inventory store IDs are valid."
            if invalid_rows.empty
            else f"{len(invalid_rows)} inventory rows have invalid store IDs."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_inventory_product_fk(
    inventory: pd.DataFrame,
    products: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate inventory product IDs against the products table."""

    invalid_rows = inventory[
        ~inventory["product_id"].isin(products["product_id"])
    ]

    dq.add_result(
        rule="Valid Inventory Product IDs",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="CRITICAL",
        records=len(invalid_rows),
        message=(
            "All inventory product IDs are valid."
            if invalid_rows.empty
            else f"{len(invalid_rows)} inventory rows have invalid product IDs."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_non_negative_inventory(
    inventory: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate that inventory quantities are not negative."""

    invalid_rows = inventory[
        inventory["quantity_on_hand"].isna()
        | (inventory["quantity_on_hand"] < 0)
    ][
        [
            "store_id",
            "product_id",
            "quantity_on_hand",
        ]
    ]

    dq.add_result(
        rule="Non-Negative Inventory Quantities",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="HIGH",
        records=len(invalid_rows),
        message=(
            "All inventory quantities are zero or greater."
            if invalid_rows.empty
            else f"{len(invalid_rows)} inventory records have invalid quantities."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_reorder_point(
    inventory: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate that reorder point are zero or greater."""

    invalid_rows = inventory[
        inventory["reorder_point"].isna()
        | (inventory["reorder_point"] < 0)
    ][
        [
            "store_id",
            "product_id",
            "reorder_point",
        ]
    ]

    dq.add_result(
        rule="Valid Inventory Reorder Point",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="MEDIUM",
        records=len(invalid_rows),
        message=(
            "All reorder point are valid."
            if invalid_rows.empty
            else f"{len(invalid_rows)} inventory records have invalid reorder point."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_inventory_transaction_ids(
    inventory_transactions: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate transaction ID uniqueness."""

    duplicate_rows = inventory_transactions[
        inventory_transactions["transaction_id"].duplicated(keep=False)
    ].sort_values("transaction_id")

    dq.add_result(
        rule="Unique Inventory Transaction IDs",
        status="PASS" if duplicate_rows.empty else "FAIL",
        severity="CRITICAL",
        records=len(duplicate_rows),
        message=(
            "All inventory transaction IDs are unique."
            if duplicate_rows.empty
            else (
                f"{len(duplicate_rows)} rows contain duplicate "
                "inventory transaction IDs."
            )
        ),
        examples=duplicate_rows.head(5).to_dict("records"),
    )


def validate_transaction_store_fk(
    inventory_transactions: pd.DataFrame,
    stores: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate transaction store IDs."""

    invalid_rows = inventory_transactions[
        ~inventory_transactions["store_id"].isin(stores["store_id"])
    ]

    dq.add_result(
        rule="Valid Inventory Transaction Store IDs",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="CRITICAL",
        records=len(invalid_rows),
        message=(
            "All inventory transaction store IDs are valid."
            if invalid_rows.empty
            else f"{len(invalid_rows)} transactions have invalid store IDs."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_transaction_product_fk(
    inventory_transactions: pd.DataFrame,
    products: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate transaction product IDs."""

    invalid_rows = inventory_transactions[
        ~inventory_transactions["product_id"].isin(products["product_id"])
    ]

    dq.add_result(
        rule="Valid Inventory Transaction Product IDs",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="CRITICAL",
        records=len(invalid_rows),
        message=(
            "All inventory transaction product IDs are valid."
            if invalid_rows.empty
            else f"{len(invalid_rows)} transactions have invalid product IDs."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_transaction_types(
    inventory_transactions: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate inventory transaction types."""

    normalized_types = (
        inventory_transactions["transaction_type"]
        .astype("string")
        .str.lower()
        .str.strip()
    )

    invalid_rows = inventory_transactions[
        normalized_types.isna()
        | ~normalized_types.isin(VALID_TRANSACTION_TYPES)
    ]

    dq.add_result(
        rule="Valid Inventory Transaction Types",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="HIGH",
        records=len(invalid_rows),
        message=(
            "All inventory transaction types are valid."
            if invalid_rows.empty
            else f"{len(invalid_rows)} transactions have invalid types."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_transaction_quantities(
    inventory_transactions: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Validate that inventory transaction quantities are not null or zero."""

    invalid_rows = inventory_transactions[
        inventory_transactions["quantity_change"].isna()
        | (inventory_transactions["quantity_change"] == 0)
    ]

    dq.add_result(
        rule="Valid Inventory Transaction Quantities",
        status="PASS" if invalid_rows.empty else "FAIL",
        severity="HIGH",
        records=len(invalid_rows),
        message=(
            "All inventory transaction quantities are non-zero."
            if invalid_rows.empty
            else f"{len(invalid_rows)} transactions contain invalid quantities."
        ),
        examples=invalid_rows.head(5).to_dict("records"),
    )


def validate_inventory(
    inventory: pd.DataFrame,
    inventory_transactions: pd.DataFrame,
    stores: pd.DataFrame,
    products: pd.DataFrame,
    dq: DataQuality,
) -> None:
    """Run all inventory validation rules."""

    validate_inventory_composite_key(inventory, dq)
    validate_inventory_store_fk(inventory, stores, dq)
    validate_inventory_product_fk(inventory, products, dq)
    validate_non_negative_inventory(inventory, dq)
    validate_reorder_point(inventory, dq)

    validate_inventory_transaction_ids(inventory_transactions, dq)
    validate_transaction_store_fk(inventory_transactions, stores, dq)
    validate_transaction_product_fk(inventory_transactions, products, dq)
    validate_transaction_types(inventory_transactions, dq)
    validate_transaction_quantities(inventory_transactions, dq)