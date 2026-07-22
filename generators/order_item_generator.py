import random
import pandas as pd


def generate_order_items(orders: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    order_items = []
    order_item_id = 1

    for order_id in orders["order_id"]:

        num_items = random.choices(
            [1, 2, 3, 4, 5],
            weights=[40, 30, 20, 8, 2],
            k=1
        )[0]

        selected_products = products.sample(num_items)

        for _, product in selected_products.iterrows():

            quantity = random.choices(
                [1, 2, 3, 4, 5],
                weights=[65, 20, 10, 4, 1],
                k=1
            )[0]

            unit_price = product["price"]
            unit_cost = product["cost"]

            line_total = round(quantity * unit_price, 2)

            order_items.append({
                "order_item_id": order_item_id,
                "order_id": order_id,
                "product_id": product["product_id"],
                "quantity": quantity,
                "unit_price": unit_price,
                "unit_cost": unit_cost,
                "line_total": line_total
            })

            order_item_id += 1

    return pd.DataFrame(order_items)