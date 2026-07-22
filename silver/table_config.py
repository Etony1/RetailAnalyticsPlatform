"""
Configuration for every Silver transformation.

Each table defines:

- datetime columns
- integer columns
- float columns
- non-negative validations
- positive validations
"""

TABLE_CONFIG = {

    "customers": {
        "datetime": ["join_date"],
        "integers": ["customer_id"],
        "floats": [],
        "non_negative": [],
        "positive": [],
    },

    "products": {
        "datetime": [],
        "integers": [
            "product_id",
            "supplier_id",
        ],
        "floats": [
            "cost",
            "price",
        ],
        "non_negative": [
            "cost",
            "price",
        ],
        "positive": [],
    },

    "orders": {
        "datetime": [
            "order_date",
        ],
        "integers": [
            "order_id",
            "customer_id",
            "store_id",
            "employee_id",
        ],
        "floats": [
            "subtotal",
            "discount_amount",
            "tax_amount",
            "shipping_fee",
            "total_amount",
            "discount_rate",
        ],
        "non_negative": [
            "subtotal",
            "discount_amount",
            "tax_amount",
            "shipping_fee",
            "total_amount",
        ],
        "positive": [],
    },

    "order_items": {
        "datetime": [],
        "integers": [
            "order_item_id",
            "order_id",
            "product_id",
            "quantity",
        ],
        "floats": [
            "unit_price",
            "unit_cost",
            "line_total",
        ],
        "non_negative": [
            "unit_price",
            "unit_cost",
            "line_total",
        ],
        "positive": [
            "quantity",
        ],
    },

    "inventory_snapshot": {
        "datetime": [
            "last_restock_date",
        ],
        "integers": [
            "inventory_id",
            "store_id",
            "product_id",
            "quantity_on_hand",
            "reorder_point",
            "reorder_quantity",
            "max_stock_level",
        ],
        "floats": [
            "inventory_value",
        ],
        "non_negative": [
            "quantity_on_hand",
            "inventory_value",
        ],
        "positive": [],
    },

    "inventory_transactions": {
        "datetime": [
            "transaction_date",
        ],
        "integers": [
            "transaction_id",
            "store_id",
            "employee_id",
            "product_id",
            "quantity_change",
            "source_order_id",
        ],
        "floats": [],
        "non_negative": [],
        "positive": [],
    },

    "returns": {
        "datetime": [
            "return_date",
        ],
        "integers": [
            "return_id",
            "source_order_id",
            "order_item_id",
            "customer_id",
            "store_id",
            "employee_id",
            "product_id",
            "quantity_returned",
        ],
        "floats": [
            "refund_amount",
        ],
        "non_negative": [
            "refund_amount",
        ],
        "positive": [
            "quantity_returned",
        ],
    },

    "employees": {
        "datetime": [
            "hire_date",
        ],
        "integers": [
            "employee_id",
            "store_id",
        ],
        "floats": [
            "salary",
        ],
        "non_negative": [
            "salary",
        ],
        "positive": [],
    },

    "stores": {
        "datetime": [],
        "integers": [
            "store_id",
        ],
        "floats": [],
        "non_negative": [],
        "positive": [],
    },

    "suppliers": {
        "datetime": [],
        "integers": [
            "supplier_id",
            "rating",
            "lead_time_days",
        ],
        "floats": [],
        "non_negative": [
            "lead_time_days",
        ],
        "positive": [
            "rating",
        ],
    },
}