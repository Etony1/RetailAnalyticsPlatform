import random
import pandas as pd
from faker import Faker

fake = Faker()

JOB_TITLES = [
    "Store Manager",
    "Assistant Manager",
    "Sales Associate",
    "Cashier",
    "Inventory Specialist",
    "Customer Service Representative"
]


def generate_employees(num_employees, num_stores):

    employees = []

    for employee_id in range(1, num_employees + 1):

        employees.append({

            "employee_id": employee_id,

            "first_name": fake.first_name(),

            "last_name": fake.last_name(),

            "email": fake.company_email(),

            "phone": fake.phone_number(),

            "job_title": random.choice(JOB_TITLES),

            "hire_date": fake.date_between(
                start_date="-10y",
                end_date="today"
            ),

            "salary": round(random.uniform(35000, 110000), 2),

            "store_id": random.randint(1, num_stores),

            "active": random.choice([True, True, True, False])

        })

    return pd.DataFrame(employees)