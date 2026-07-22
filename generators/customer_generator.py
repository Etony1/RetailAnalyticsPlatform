import random
import pandas as pd
from faker import Faker

fake = Faker()

def generate_customers(num_customers: int) -> pd.DataFrame:
    customers = []
    loyalty_levels = ["Bronze", "Silver", "Gold", "Platinum"]

    for customer_id in range(1, num_customers + 1):
        customers.append({
            "customer_id": customer_id,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "city": fake.city(),
            "state": fake.state(),
            "zip_code": fake.postcode(),
            "join_date": fake.date_between(start_date="-5y", end_date="today"),
            "loyalty_level": random.choice(loyalty_levels)
        })

    return pd.DataFrame(customers)