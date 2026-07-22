import random
import pandas as pd
from faker import Faker

fake = Faker()

def generate_orders(num_orders, num_customers, num_stores, num_employees):
    statuses = ["Completed", "Pending", "Cancelled", "Returned"]
    payment_methods = ["Credit Card", "Debit Card", "Cash", "Gift Card", "Mobile Payment"]

    orders = []

    for order_id in range(1, num_orders + 1):
        orders.append({
            "order_id": order_id,
            "customer_id": random.randint(1, num_customers),
            "store_id": random.randint(1, num_stores),
            "employee_id": random.randint(1, num_employees),
            "order_date": fake.date_between(start_date="-2y", end_date="today"),
            "order_status": random.choices(
                statuses,
                weights=[85, 8, 4, 3],
                k=1
            )[0],
            "payment_method": random.choice(payment_methods),
            "subtotal": 0.00,
            "tax_amount": 0.00,
            "shipping_fee": 0.00,
            "discount_amount": 0.00,
            "total_amount": 0.00
        })

    return pd.DataFrame(orders)

# subtotal = sum(line_total) per order
# tax_amount = subtotal * 0.08
# shipping_fee = simple shipping rule
# discount_amount = simple discount rule
# total_amount = subtotal + tax + shipping - discount