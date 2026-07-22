import random
import pandas as pd
from faker import Faker

fake = Faker()


def generate_suppliers(num_suppliers: int) -> pd.DataFrame:

    payment_terms = [
        "Net 30",
        "Net 45",
        "Net 60",
        "Due on Receipt"
    ]

    countries = [
        "USA",
        "Canada",
        "Mexico",
        "Germany",
        "China",
        "Japan",
        "South Korea"
    ]

    suppliers = []

    for supplier_id in range(1, num_suppliers + 1):

        suppliers.append({

            "supplier_id": supplier_id,

            "supplier_name": fake.company(),

            "contact_name": fake.name(),

            "country": random.choice(countries),

            "rating": random.randint(3, 5),

            "lead_time_days": random.randint(2, 30),

            "payment_terms": random.choice(payment_terms),

            "active": random.choice([True, True, True, False])

        })

    return pd.DataFrame(suppliers)