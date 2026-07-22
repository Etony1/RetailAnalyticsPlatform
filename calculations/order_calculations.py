# import pandas as pd


# def calculate_order_totals(orders, order_items):

#     subtotal = (
#         order_items
#         .groupby("order_id")["line_total"]
#         .sum()
#         .reset_index()
#     )

#     subtotal.rename(
#         columns={
#             "line_total": "subtotal"
#         },
#         inplace=True
#     )

#     orders = orders.merge(
#         subtotal,
#         on="order_id",
#         how="left",
#         suffixes=("", "_new")
#     )

#     orders["subtotal"] = orders["subtotal_new"]
#     orders["tax_amount"] = round(orders["subtotal"] * 0.08, 2)

#     orders.drop(
#         columns=["subtotal_new"],
#         inplace=True
#     )

#     return orders


# import pandas as pd

# # -------------------------------------------------
# # Subtotal
# # -------------------------------------------------

# def calculate_subtotal(orders, order_items):

#     subtotal = (
#         order_items
#         .groupby("order_id")["line_total"]
#         .sum()
#         .reset_index()
#         .rename(columns={"line_total": "subtotal"})
#     )

#     orders = orders.drop(columns=["subtotal"], errors="ignore")

#     orders = orders.merge(
#         subtotal,
#         on="order_id",
#         how="left"
#     )

#     return orders

# # -------------------------------------------------
# # Tax
# # -------------------------------------------------

# def calculate_tax(orders):

#     orders["tax_amount"] = (
#         orders["subtotal"] * 0.08
#     ).round(2)

#     return orders

# # -------------------------------------------------
# # Shipping
# # -------------------------------------------------

# def calculate_shipping(orders):

#     orders["shipping_fee"] = orders["subtotal"].apply(
#         lambda x: 0 if x >= 100 else 9.99
#     )

#     return orders

# # -------------------------------------------------
# # Discount
# # -------------------------------------------------

# def calculate_discount(orders):

#     orders["discount_amount"] = 0

#     return orders


# # -------------------------------------------------
# # Total
# # -------------------------------------------------

# def calculate_total(orders):

#     orders["total_amount"] = (

#         orders["subtotal"]

#         + orders["tax_amount"]

#         + orders["shipping_fee"]

#         - orders["discount_amount"]

#     ).round(2)

#     return orders

# def calculate_order_totals(orders, order_items):

#     orders = calculate_subtotal(orders, order_items)

#     orders = calculate_discount(orders)

#     orders = calculate_tax(orders)

#     orders = calculate_shipping(orders)

#     orders = calculate_total(orders)

#     return orders    




import pandas as pd


def calculate_subtotal(orders, order_items):
    subtotal = (
        order_items
        .groupby("order_id")["line_total"]
        .sum()
        .reset_index()
        .rename(columns={"line_total": "subtotal"})
    )

    orders = orders.drop(columns=["subtotal"], errors="ignore")

    orders = orders.merge(
        subtotal,
        on="order_id",
        how="left"
    )

    return orders


def calculate_discount(orders, customers):
    loyalty_discount = {
        "Bronze": 0.00,
        "Silver": 0.05,
        "Gold": 0.10,
        "Platinum": 0.15
    }

    customer_loyalty = customers[["customer_id", "loyalty_level"]]

    orders = orders.merge(
        customer_loyalty,
        on="customer_id",
        how="left"
    )

    orders["discount_rate"] = orders["loyalty_level"].map(loyalty_discount)

    orders["discount_amount"] = (
        orders["subtotal"] * orders["discount_rate"]
    ).round(2)

    return orders


def calculate_tax(orders, stores):
    tax_rates = {

    "Illinois": 0.1025,

    "Texas": 0.0825,

    "Washington": 0.065,

    "Arizona": 0.086,

    "Colorado": 0.029,

    "Georgia": 0.04,

    "Massachusetts": 0.0625,

    "New York": 0.08875

}

    orders = orders.merge(

        stores[["store_id", "state"]],

        on="store_id",

        how="left"

)

    orders["tax_rate"] = (

        orders["state"]

        .map(tax_rates)

)
    orders["tax_amount"] = (
        orders["subtotal"] * orders["tax_rate"]
        ).round(2)

    return orders


def calculate_shipping(orders):
    orders["shipping_fee"] = orders["subtotal"].apply(
        lambda x: 0 if x >= 100 else 9.99
    )

    return orders


def calculate_total(orders):
    orders["total_amount"] = (
        orders["subtotal"]
        + orders["tax_amount"]
        + orders["shipping_fee"]
        - orders["discount_amount"]
    ).round(2)

    return orders


def calculate_order_totals(orders, order_items, customers, stores):
    orders = calculate_subtotal(orders, order_items)
    orders = calculate_discount(orders, customers)
    orders = calculate_tax(orders, stores)
    orders = calculate_shipping(orders)
    orders = calculate_total(orders)


    column_order = ["order_id","customer_id","store_id","employee_id","order_date","order_status",
    "payment_method","loyalty_level","discount_rate","subtotal","discount_amount",
    "tax_amount","shipping_fee","total_amount"]

    orders = orders[column_order]

    return orders