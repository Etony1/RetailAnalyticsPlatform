# from config import NUM_CUSTOMERS, NUM_PRODUCTS, RAW_DATA_DIR

# from generators.customer_generator import generate_customers
# from generators.product_generator import generate_products
# from generators.store_generator import generate_stores
# from generators.supplier_generator import generate_suppliers
# print("=" * 50)
# print("Retail Analytics Platform")
# print("=" * 50)

# # Customers
# customers = generate_customers(NUM_CUSTOMERS)
# customers.to_csv(RAW_DATA_DIR / "customers.csv", index=False)

# print(f"Generated {len(customers)} customers")

# # Products
# products = generate_products(NUM_PRODUCTS)
# products.to_csv(RAW_DATA_DIR / "products.csv", index=False)

# print(f"Generated {len(products)} products")

# print("\nData generation complete!")

# # -------------------------
# # Stores
# # -------------------------

# stores = generate_stores()

# print("\nSTORES")
# print(stores)

# print(f"\nRows: {stores.shape[0]}")
# print(f"Columns: {stores.shape[1]}")

# stores.to_csv(
#     RAW_DATA_DIR / "stores.csv",
#     index=False
# )


# # -------------------------
# # Suppliers
# # -------------------------

# suppliers = generate_suppliers(NUM_SUPPLIERS)

# print("\nSUPPLIERS")
# print(suppliers.head())

# suppliers.to_csv(
#     RAW_DATA_DIR / "suppliers.csv",
#     index=False
# )

# print(f"Generated {len(suppliers)} suppliers")


# from config import *
# from generators.customer_generator import generate_customers
# from generators.product_generator import generate_products
# from generators.store_generator import generate_stores
# from generators.supplier_generator import generate_suppliers

# from utils.file_utils import save_dataframe


# customers = generate_customers(NUM_CUSTOMERS)
# save_dataframe(customers, RAW_DATA_DIR, "customers.csv")

# products = generate_products(NUM_PRODUCTS)
# save_dataframe(products, RAW_DATA_DIR, "products.csv")

# stores = generate_stores()
# save_dataframe(stores, RAW_DATA_DIR, "stores.csv")

# suppliers = generate_suppliers(NUM_SUPPLIERS)
# save_dataframe(suppliers, RAW_DATA_DIR, "suppliers.csv")



"""
Retail Analytics Platform
Master Data Generator
"""

# =====================================
# Imports
# =====================================

from config import *

from generators.customer_generator import generate_customers
from generators.product_generator import generate_products
from generators.store_generator import generate_stores
from generators.supplier_generator import generate_suppliers
from generators.employee_generator import generate_employees
from generators.order_generator import generate_orders
from generators.order_item_generator import generate_order_items
from calculations.order_calculations import calculate_order_totals
from generators.inventory_generator import generate_inventory
from generators.inventory_transaction_generator import generate_inventory_transactions
from generators.return_generator import generate_returns
from processors.inventory_processor import update_inventory_snapshot

from validations.data_quality import DataQuality
from validations.customer_validation import validate_customers
from validations.product_validation import validate_products
from validations.order_validation import validate_orders
from validations.inventory_validation import validate_inventory
from validations.return_validation import validate_returns

from utils.file_utils import save_dataframe

# =====================================
# Main
# =====================================

def main():

    print("=" * 60)
    print("Retail Analytics Platform")
    print("=" * 60)

    # --------------------------
    # Customers
    # --------------------------

    customers = generate_customers(NUM_CUSTOMERS)
    save_dataframe(customers, RAW_DATA_DIR, "customers.csv")
    # print("\n===== CUSTOMERS =====")
    # print(customers.columns.tolist())

    # --------------------------
    # Suppliers
    # --------------------------

    suppliers = generate_suppliers(NUM_SUPPLIERS)
    save_dataframe(suppliers, RAW_DATA_DIR, "suppliers.csv")

    # --------------------------
    # Products
    # --------------------------

    products = generate_products(NUM_PRODUCTS,len(suppliers))
    save_dataframe(products, RAW_DATA_DIR, "products.csv")
    # print("\n===== PRODUCTS =====")
    # print(products.columns.tolist())

    # --------------------------
    # Stores
    # --------------------------

    stores = generate_stores()
    save_dataframe(stores, RAW_DATA_DIR, "stores.csv")


    # --------------------------
    # employee
    # --------------------------
    employees = generate_employees(NUM_EMPLOYEES, len(stores))
    save_dataframe(employees, RAW_DATA_DIR,  "employees.csv")

    # --------------------------
    # order
    # --------------------------

    orders = generate_orders(NUM_ORDERS, len(customers), len(stores), len(employees))
    # save_dataframe(orders, RAW_DATA_DIR, "orders.csv")
    # print("\n===== ORDERS =====")
    # print(orders.columns.tolist())    

    # --------------------------
    # order_item
    # --------------------------

    order_items = generate_order_items(orders, products)
    # save_dataframe(order_items, RAW_DATA_DIR, "order_items.csv")
    # print("\n===== ORDER ITEMS =====")
    # print(order_items.columns.tolist())

    # --------------------------
    # inventory
    # --------------------------
    inventory = generate_inventory(stores, products )
    save_dataframe(inventory, RAW_DATA_DIR, "inventory_snapshot.csv")
    # print("\n===== INVENTORY =====")
    # print(inventory.columns.tolist())
    # --------------------------
    # inventory_transaction
    # --------------------------


    inventory_transactions = generate_inventory_transactions(orders, order_items)
    save_dataframe(inventory_transactions, RAW_DATA_DIR, "inventory_transactions.csv")
    # print("\n===== INVENTORY TRANSACTIONS =====")
    # print(inventory_transactions.columns.tolist())
    # --------------------------
    # inventory_processor
    # --------------------------
    updated_inventory = update_inventory_snapshot(inventory, inventory_transactions, products)
    save_dataframe(updated_inventory, RAW_DATA_DIR, "inventory_snapshot_updated.csv")

    # --------------------------
    # returns
    # --------------------------
    returns = generate_returns(orders, order_items)
    save_dataframe(returns, RAW_DATA_DIR, "returns.csv")
    # print("\n===== RETURNS =====")
    # print(returns.columns.tolist())
    # --------------------------
    # calculations
    # --------------------------
    # orders = calculate_order_totals(orders, order_items)
    orders = calculate_order_totals(orders, order_items, customers, stores)
    save_dataframe(orders, RAW_DATA_DIR, "orders.csv")
    save_dataframe(order_items, RAW_DATA_DIR, "order_items.csv")

    # check = inventory.merge(updated_inventory, on=["store_id", "product_id"], suffixes=("_before", "_after"))

    # movements = (inventory_transactions.groupby(["store_id", "product_id"])["quantity_change"]
    # .sum()
    # .reset_index()
    # .rename(columns={"quantity_change": "net_movement"}))

    # check = check.merge(
    # movements,
    # on=["store_id", "product_id"],
    # how="left")

    # check["net_movement"] = check["net_movement"].fillna(0)

    # check["expected_after"] = (
    # check["quantity_on_hand_before"] + check["net_movement"])

    # mismatch = check[
    # check["quantity_on_hand_after"] != check["expected_after"]]

    # print("Inventory mismatches:", len(mismatch))

    # print(
    # mismatch[
    #     [
    #         "store_id",
    #         "product_id",
    #         "quantity_on_hand_before",
    #         "net_movement",
    #         "quantity_on_hand_after",
    #         "expected_after"
    #     ]    ].head(20))


    print("=" * 60)
    print("Master data generation complete!")
    print("=" * 60)
    
    

    

    

    

    

    

    
    # =====================================
    # Data Quality Validation
    # =====================================

    # customers

    dq = DataQuality()

    # validate_customers(customers, dq)

    # dq.report()

    # dq.save_report(
    #     RAW_DATA_DIR / "data_quality_report.csv"
    # )

    # # product

    # dq = DataQuality()

    # # validate_customers(customers, dq)
    # validate_products(products, suppliers, dq)

    # dq.report()

    # dq.save_report(
    # RAW_DATA_DIR / "data_quality_report.csv"
    # )


    # validate_orders(orders=orders,order_items=order_items,customers=customers,stores=stores,employees=employees,dq=dq,)

    # validate_inventory(inventory=inventory,inventory_transactions=inventory_transactions,stores=stores,products=products,dq=dq,)

    # validate_returns(returns=returns,orders=orders,order_items=order_items,products=products,dq=dq,)

    validate_customers(
        customers=customers,
        dq=dq,
    )

    validate_products(
        products=products,
        suppliers=suppliers,
        dq=dq,
    )

    validate_orders(
        orders=orders,
        order_items=order_items,
        customers=customers,
        stores=stores,
        employees=employees,
        dq=dq,
    )

    validate_inventory(
        inventory=inventory,
        inventory_transactions=inventory_transactions,
        stores=stores,
        products=products,
        dq=dq,
    )

    validate_returns(
        returns=returns,
        orders=orders,
        order_items=order_items,
        products=products,
        dq=dq,
    )

    # print(
    #     [
    #         method
    #         for method in dir(dq)
    #         if not method.startswith("_")
    #     ]
    # )
    dq.report()
    dq.save_report(RAW_DATA_DIR / "data_quality_report.csv")
    # dq.summary()

if __name__ == "__main__":
    main()

