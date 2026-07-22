import random
import pandas as pd
from datetime import timedelta


RETURN_REASONS = [
    "Damaged",
    "Wrong Item",
    "Customer Changed Mind",
    "Defective",
    "Late Delivery",
    "Wrong Size"
]


def generate_returns(orders, order_items):

    returns = []

    return_id = 1

    for _, item in order_items.iterrows():

        # About 8% of items are returned
        if random.random() > 0.08:
            continue

        order = orders.loc[
            orders["order_id"] == item["order_id"]
        ].iloc[0]

        quantity_returned = random.randint(
            1,
            item["quantity"]
        )

        return_date = (
            pd.to_datetime(order["order_date"])
            +
            timedelta(days=random.randint(1, 30))
        )

        refund_amount = round(
            quantity_returned * item["unit_price"],
            2
        )

        returns.append({

            "return_id": return_id,

            "source_order_id": item["order_id"],

            "order_item_id": item["order_item_id"],

            "customer_id": order["customer_id"],

            "store_id": order["store_id"],

            "employee_id": order["employee_id"],

            "product_id": item["product_id"],

            "return_date": return_date,

            "quantity_returned": quantity_returned,

            "return_reason": random.choice(
                RETURN_REASONS
            ),

            "refund_amount": refund_amount

        })

        return_id += 1

    return pd.DataFrame(returns)