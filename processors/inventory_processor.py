import pandas as pd


def recalculate_inventory_status(row):
    if row["quantity_on_hand"] <= row["reorder_point"]:
        return "Low Stock"
    elif row["quantity_on_hand"] >= row["max_stock_level"]:
        return "Overstock"
    else:
        return "Healthy"


def update_inventory_snapshot(inventory_snapshot, inventory_transactions, products):
    net_movement = (
        inventory_transactions
        .groupby(["store_id", "product_id"])["quantity_change"]
        .sum()
        .reset_index()
        .rename(columns={"quantity_change": "net_movement"})
    )

    updated_inventory = inventory_snapshot.merge(
        net_movement,
        on=["store_id", "product_id"],
        how="left"
    )

    updated_inventory["net_movement"] = updated_inventory["net_movement"].fillna(0)

    updated_inventory["quantity_on_hand"] = (
        updated_inventory["quantity_on_hand"] + updated_inventory["net_movement"]
    )

    updated_inventory["quantity_on_hand"] = updated_inventory["quantity_on_hand"].clip(lower=0)

    product_costs = products[["product_id", "cost"]]

    updated_inventory = updated_inventory.merge(
        product_costs,
        on="product_id",
        how="left"
    )

    updated_inventory["inventory_value"] = (
        updated_inventory["quantity_on_hand"] * updated_inventory["cost"]
    ).round(2)

    updated_inventory["inventory_status"] = updated_inventory.apply(
        recalculate_inventory_status,
        axis=1
    )

    updated_inventory = updated_inventory.drop(
        columns=["net_movement", "cost"],
        errors="ignore"
    )

    return updated_inventory