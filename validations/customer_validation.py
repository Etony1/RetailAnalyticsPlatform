def validate_customers(customers, dq):
    """
    Run all customer data-quality checks.
    """

    # -------------------------------------------------
    # Rule 1: Customer IDs must be unique
    # -------------------------------------------------
    duplicate_ids = customers[
        customers["customer_id"].duplicated(keep=False)
    ]

    if duplicate_ids.empty:
        dq.add_result(
            rule="Unique Customer IDs",
            status="PASS",
            severity="CRITICAL",
            records=0,
            message="All customer IDs are unique."
        )
    else:
        examples = (
            duplicate_ids["customer_id"]
            .drop_duplicates()
            .head(10)
            .tolist()
        )

        dq.add_result(
            rule="Unique Customer IDs",
            status="FAIL",
            severity="CRITICAL",
            records=len(duplicate_ids),
            message="Duplicate customer IDs were found.",
            examples=examples
        )

    # -------------------------------------------------
    # Rule 2: Customer emails must be unique
    # -------------------------------------------------
    duplicate_emails = customers[
        customers["email"].duplicated(keep=False)
    ]

    if duplicate_emails.empty:
        dq.add_result(
            rule="Unique Customer Emails",
            status="PASS",
            severity="CRITICAL",
            records=0,
            message="All customer emails are unique."
        )
    else:
        examples = (
            duplicate_emails["email"]
            .drop_duplicates()
            .head(10)
            .tolist()
        )

        dq.add_result(
            rule="Unique Customer Emails",
            status="FAIL",
            severity="CRITICAL",
            records=len(duplicate_emails),
            message="Duplicate customer emails were found.",
            examples=examples
        )

    # -------------------------------------------------
    # Rule 3: State cannot be missing
    # -------------------------------------------------
    missing_states = customers[
        customers["state"].isna()
        | customers["state"].astype(str).str.strip().eq("")
    ]

    if missing_states.empty:
        dq.add_result(
            rule="Customer State Completeness",
            status="PASS",
            severity="HIGH",
            records=0,
            message="All customers have a state."
        )
    else:
        examples = (
            missing_states["customer_id"]
            .head(10)
            .tolist()
        )

        dq.add_result(
            rule="Customer State Completeness",
            status="FAIL",
            severity="HIGH",
            records=len(missing_states),
            message="Some customers have a missing state.",
            examples=examples
        )

    # -------------------------------------------------
    # Rule 4: Loyalty level must be valid
    # -------------------------------------------------
    valid_loyalty_levels = {
        "Bronze",
        "Silver",
        "Gold",
        "Platinum"
    }

    invalid_loyalty = customers[
        ~customers["loyalty_level"].isin(valid_loyalty_levels)
    ]

    if invalid_loyalty.empty:
        dq.add_result(
            rule="Valid Customer Loyalty Levels",
            status="PASS",
            severity="HIGH",
            records=0,
            message="All customer loyalty levels are valid."
        )
    else:
        examples = (
            invalid_loyalty[
                ["customer_id", "loyalty_level"]
            ]
            .head(10)
            .to_dict("records")
        )

        dq.add_result(
            rule="Valid Customer Loyalty Levels",
            status="FAIL",
            severity="HIGH",
            records=len(invalid_loyalty),
            message="Invalid customer loyalty levels were found.",
            examples=examples
        )