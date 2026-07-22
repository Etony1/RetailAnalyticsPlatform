import pandas as pd


def generate_inventory_transactions(orders, order_items):

    # Join order items to order headers
    transactions = order_items.merge(
        orders[
            [
                "order_id",
                "store_id",
                "employee_id",
                "order_date"
            ]
        ],
        on="order_id",
        how="left"
    )

    # Rename columns
    transactions = transactions.rename(
        columns={
            "order_date": "transaction_date",
            "order_id": "source_order_id"
        }
    )

    # Create transaction ID
    transactions.insert(
        0,
        "transaction_id",
        range(1, len(transactions) + 1)
    )

    # Sale reduces inventory
    transactions["quantity_change"] = (
        transactions["quantity"] * -1
    )

    transactions["transaction_type"] = "Sale"

    # Select final columns
    transactions = transactions[
        [
            "transaction_id",
            "transaction_date",
            "store_id",
            "employee_id",
            "product_id",
            "transaction_type",
            "quantity_change",
            "source_order_id"
        ]
    ]

    return transactions