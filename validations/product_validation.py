def validate_products(products, suppliers, dq):
    """
    Run all product data-quality checks.
    """

    # -------------------------------------------------
    # Rule 1: Product IDs must be unique
    # -------------------------------------------------
    duplicate_ids = products[
        products["product_id"].duplicated(keep=False)
    ]

    if duplicate_ids.empty:
        dq.add_result(
            rule="Unique Product IDs",
            status="PASS",
            severity="CRITICAL",
            records=0,
            message="All product IDs are unique."
        )
    else:
        examples = (
            duplicate_ids["product_id"]
            .drop_duplicates()
            .head(10)
            .tolist()
        )

        dq.add_result(
            rule="Unique Product IDs",
            status="FAIL",
            severity="CRITICAL",
            records=len(duplicate_ids),
            message="Duplicate product IDs were found.",
            examples=examples
        )

    # -------------------------------------------------
    # Rule 2: Price must be greater than cost
    # -------------------------------------------------
    invalid_margin = products[
        products["price"] <= products["cost"]
    ]

    if invalid_margin.empty:
        dq.add_result(
            rule="Product Price Greater Than Cost",
            status="PASS",
            severity="CRITICAL",
            records=0,
            message="All product prices are greater than product costs."
        )
    else:
        examples = (
            invalid_margin[
                ["product_id", "cost", "price"]
            ]
            .head(10)
            .to_dict("records")
        )

        dq.add_result(
            rule="Product Price Greater Than Cost",
            status="FAIL",
            severity="CRITICAL",
            records=len(invalid_margin),
            message="Some products have a price less than or equal to cost.",
            examples=examples
        )

    # -------------------------------------------------
    # Rule 3: Prices must be positive
    # -------------------------------------------------
    invalid_prices = products[
        products["price"] <= 0
    ]

    if invalid_prices.empty:
        dq.add_result(
            rule="Positive Product Prices",
            status="PASS",
            severity="CRITICAL",
            records=0,
            message="All product prices are positive."
        )
    else:
        examples = (
            invalid_prices[
                ["product_id", "price"]
            ]
            .head(10)
            .to_dict("records")
        )

        dq.add_result(
            rule="Positive Product Prices",
            status="FAIL",
            severity="CRITICAL",
            records=len(invalid_prices),
            message="Non-positive product prices were found.",
            examples=examples
        )

    # -------------------------------------------------
    # Rule 4: Costs must be positive
    # -------------------------------------------------
    invalid_costs = products[
        products["cost"] <= 0
    ]

    if invalid_costs.empty:
        dq.add_result(
            rule="Positive Product Costs",
            status="PASS",
            severity="CRITICAL",
            records=0,
            message="All product costs are positive."
        )
    else:
        examples = (
            invalid_costs[
                ["product_id", "cost"]
            ]
            .head(10)
            .to_dict("records")
        )

        dq.add_result(
            rule="Positive Product Costs",
            status="FAIL",
            severity="CRITICAL",
            records=len(invalid_costs),
            message="Non-positive product costs were found.",
            examples=examples
        )

    # -------------------------------------------------
    # Rule 5: Supplier IDs must exist
    # -------------------------------------------------
    valid_supplier_ids = set(
        suppliers["supplier_id"]
    )

    invalid_suppliers = products[
        ~products["supplier_id"].isin(valid_supplier_ids)
    ]

    if invalid_suppliers.empty:
        dq.add_result(
            rule="Valid Product Supplier IDs",
            status="PASS",
            severity="CRITICAL",
            records=0,
            message="All product supplier IDs exist in the suppliers table."
        )
    else:
        examples = (
            invalid_suppliers[
                ["product_id", "supplier_id"]
            ]
            .head(10)
            .to_dict("records")
        )

        dq.add_result(
            rule="Valid Product Supplier IDs",
            status="FAIL",
            severity="CRITICAL",
            records=len(invalid_suppliers),
            message="Some products reference supplier IDs that do not exist.",
            examples=examples
        )