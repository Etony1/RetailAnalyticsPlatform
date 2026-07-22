import random
import pandas as pd
from faker import Faker

fake = Faker()


def generate_inventory(stores, products):

    inventory = []

    inventory_id = 1

    for _, store in stores.iterrows():

        for _, product in products.iterrows():

            quantity = random.randint(20, 300)

            reorder_point = random.randint(15, 40)

            reorder_quantity = random.randint(50, 200)

            max_stock = random.randint(250, 500)

            inventory_value = round(
                quantity * product["cost"],
                2
            )

            inventory.append({

                "inventory_id": inventory_id,

                "store_id": store["store_id"],

                "product_id": product["product_id"],

                "quantity_on_hand": quantity,

                "reorder_point": reorder_point,

                "reorder_quantity": reorder_quantity,

                "max_stock_level": max_stock,

                "inventory_value": inventory_value,

                "last_restock_date": fake.date_between(
                    start_date="-90d",
                    end_date="today"
                )

            })

            inventory_id += 1

    return pd.DataFrame(inventory)