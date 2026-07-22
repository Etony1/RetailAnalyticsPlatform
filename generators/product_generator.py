# this is for product
import random
import pandas as pd


# def generate_products(num_products: int) -> pd.DataFrame:
def generate_products(num_products: int,num_suppliers: int) -> pd.DataFrame:    

    categories = {
        "Electronics": [
            "Laptop",
            "Monitor",
            "Keyboard",
            "Mouse",
            "Headphones",
            "Tablet",
            "Printer"
        ],

        "Furniture": [
            "Office Chair",
            "Desk",
            "Bookshelf",
            "Cabinet"
        ],

        "Kitchen": [
            "Coffee Maker",
            "Blender",
            "Toaster",
            "Microwave"
        ],

        "Sports": [
            "Football",
            "Basketball",
            "Yoga Mat",
            "Dumbbells"
        ],

        "Clothing": [
            "T-Shirt",
            "Jeans",
            "Jacket",
            "Sneakers"
        ]
    }

    brands = [
        "Nike",
        "Samsung",
        "Dell",
        "HP",
        "Apple",
        "Sony",
        "KitchenPro",
        "OfficeMax",
        "FitLife"
    ]

    products = []

    for product_id in range(1, num_products + 1):

        category = random.choice(list(categories.keys()))

        product_name = random.choice(categories[category])

        cost = round(random.uniform(5, 500), 2)

        markup = random.uniform(1.2, 2.0)

        price = round(cost * markup, 2)

        supplier_id = random.randint(1, num_suppliers)

        # supplier_id = random.randint(1, 100)

        products.append({

            "product_id": product_id,

            "product_name": product_name,

            "category": category,

            "brand": random.choice(brands),

            "cost": cost,

            "price": price,

            "supplier_id": supplier_id,

            "active": True

        })

    return pd.DataFrame(products)