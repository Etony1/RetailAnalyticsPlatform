# Retail Analytics Platform
## Learning Journal

---

# Sprint 1 – Project Setup

## What I built

- Created the RetailAnalyticsPlatform project.
- Created a Python virtual environment.
- Installed project dependencies.
- Created the project folder structure.
- Configured VS Code for development.

## What I learned

- How Python virtual environments work.
- Why dependencies should be isolated.
- How to troubleshoot Python installation issues.
- How to configure VS Code to use the correct interpreter.

## Interview takeaway

I can explain how to set up a professional Python project with a virtual environment, dependency management, and a structured folder layout.

---

# Sprint 2 – Master Data Generation

## What I built

Generated master data tables:

- Customers
- Products
- Stores
- Suppliers
- Employees

## What I learned

- Difference between master data and transactional data.
- Why master tables change infrequently.
- How primary keys uniquely identify business entities.
- How Faker can generate realistic sample data.

## Interview takeaway

I understand how master data supports transactional systems and why it should be modeled separately.

---

# Sprint 3 – Orders

## What I built

Created the Orders table.

Included:

- Customer
- Store
- Employee
- Order Date
- Order Status
- Payment Method

## What I learned

- One order should have one header row.
- Orders represent business events.
- Primary and foreign keys connect tables.
- Orders should not duplicate customer information.

## Interview takeaway

I can explain why Orders and Customers are separate tables and how foreign keys reduce redundancy.

---

# Sprint 4 – Order Items

## What I built

Created the Order Items table.

Each order contains multiple products.

## What I learned

- Difference between Order Header and Order Detail.
- One-to-many relationships.
- Database normalization.
- Table grain.

## Interview takeaway

I can explain why Order Items stores one row per product purchased instead of multiple products in one field.

---

# Sprint 5 – Business Calculations

## What I built

Implemented:

- Subtotal calculation
- Discount calculation
- Shipping calculation
- Tax calculation
- Total calculation

Created a separate calculations module.

## What I learned

- Business logic should be separated from data generation.
- Single Responsibility Principle.
- Derived columns.
- Reusable functions.

## Interview takeaway

I understand why business calculations belong in a dedicated module instead of the data generators.

---

# Sprint 6 – Customer Loyalty

## What I built

Implemented customer loyalty discounts.

Bronze

Silver

Gold

Platinum

## What I learned

- Joining DataFrames.
- Looking up customer attributes.
- Mapping business rules.
- Applying discounts dynamically.

## Interview takeaway

I can explain how customer master data is joined to transactional data to calculate discounts.

---

# Sprint 7 – State Tax

## What I built

Implemented state-based tax calculations.

## What I learned

- Joining Orders with Stores.
- Business rules based on geography.
- Lookup tables.
- Data enrichment.

## Interview takeaway

I understand how transactional data can be enriched using dimension tables.

---

# Sprint 8 – Inventory Snapshot

## What I built

Created Inventory Snapshot.

One row represents:

One Product

in

One Store

## What I learned

- Snapshot tables represent current state.
- Composite business keys.
- Inventory valuation.
- Inventory status.

## Interview takeaway

I can explain the difference between storing inventory by product versus product per store.

---

# Sprint 9 – Inventory Transactions

## What I built

Created Inventory Transactions.

Sales now generate inventory movement records.

## What I learned

- Event-driven design.
- Inventory ledger.
- Data lineage.
- Transaction history.
- Append-only design.

## Interview takeaway

I can explain why inventory transactions are append-only and why history should never be overwritten.

---

# Sprint 10 – Database Design

## What I learned

Major concepts:

- Database normalization
- Fact tables
- Dimension tables
- Table grain
- Composite keys
- Surrogate keys
- Business keys
- Event tables
- Snapshot tables
- One-to-many relationships
- Data lineage
- Business rules
- ETL thinking

## Interview takeaway

I now understand how to design a normalized relational database before writing code.

---

# Biggest Lessons So Far

## Data Engineering

- Design before coding.
- Define table grain first.
- Separate master and transactional data.
- Never duplicate business data.
- Record business events instead of modifying history.
- Build reusable business logic.
- Store the lowest level of detail.
- Aggregate for reporting.

---

## Software Engineering

- Separate responsibilities.
- Keep functions small.
- Organize code into modules.
- Write reusable code.
- Think about maintainability.

---

## Business Thinking

Every table exists to answer business questions.

Customers answer:

Who buys?

Orders answer:

Who bought?

Order Items answer:

What did they buy?

Inventory answers:

What do we currently have?

Inventory Transactions answer:

What happened?

Returns answer:

What was returned?

---

# Next Steps

- Returns
- Inventory updates
- Purchase Orders
- Shipments
- Data Quality Validation
- Databricks Bronze Layer
- Databricks Silver Layer
- Databricks Gold Layer
- Power BI Dashboards



                        Retail Analytics Platform

                                   Business Rules
                                         │
         ┌───────────────────────────────┼───────────────────────────────┐
         │                               │                               │
         ▼                               ▼                               ▼

 Master Data                     Transaction Data                Reference Data

 Customers                        Orders                         Stores

 Products                         Order Items                    Suppliers

 Employees                        Returns

                                   │
                                   ▼

                          Business Calculations

                       Discounts

                       Tax

                       Shipping

                       Totals

                                   │
                                   ▼

                          Inventory Processing

                      Inventory Transactions

                      Inventory Snapshot

                      Inventory Update Engine

                                   │
                                   ▼

                         Data Quality Framework

                     Customer Validation

                     Product Validation

                     Order Validation

                     Inventory Validation

                     Return Validation

                                   │
                                   ▼

                         Databricks Medallion

                     Bronze

                     Silver

                     Gold

                                   │
                                   ▼

                           Executive Dashboards




def validate_store_fk(orders, stores, dq):

    invalid_store = orders[ orders["store_id"].isin(stores["store_id"])

    ]

    if invalida_stores.empty:
        dp.add_result(
            rule="Valid store",
            status="PASS",
            severity="CRITICAL",
            records=0,
            message="all orders reference valid stores.")
    else:
        example = (invalid_stores["store_id"].drop-dup;icates().heads(10).tolist()
        )

        dp.add_result(
            rule="Valid store IDs",
            status="FAIL"
            severity="CRITICAL",
            record=len(invalid_stores),
            message="some orders reference stores that do not exist.",
            examples=examples
        )


def validate_employees_fk(orders, employees, dq):

    invalid_employees = ~orders[ orders["employee_id"].isin(employees["employee_id"])

    ]

    if invalid_employee.empty:
        dq.add_result(
            rule="Valid employees",
            status="PASS",
            severity="CRITICAL",
            records=0,
            message="all orders reference valid employees.")
    else:
        example = (invalid_employees["employee_id"]
        .drop-duplicates()
        .heads(10)
        .tolist()
        )

        dq.add_result(
            rule="Valid employee IDs",
            status="FAIL",
            severity="CRITICAL",
            records=len(invalid_employees),
            message="some orders reference employees that do not exist.",
            examples = examples
        )                          


def validate_employee_fk(orders, employees, dq):

    invalid_employees = orders[
        ~orders["employee_id"].isin(
            employees["employee_id"]
        )
    ]

    if invalid_employees.empty:
        dq.add_result(
            rule="Valid Employee IDs",
            status="PASS",
            severity="CRITICAL",
            records=0,
            message="All orders reference valid employees."
        )

    else:
        examples = (
            invalid_employees["employee_id"]
            .drop_duplicates()
            .head(10)
            .tolist()
        )

        dq.add_result(
            rule="Valid Employee IDs",
            status="FAIL",
            severity="CRITICAL",
            records=len(invalid_employees),
            message="Some orders reference employees that do not exist.",
            examples=examples
        )