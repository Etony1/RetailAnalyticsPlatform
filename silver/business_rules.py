from __future__ import annotations

import pandas as pd


def apply_business_rules(
    df: pd.DataFrame,
    table_name: str,
) -> pd.DataFrame:
    """
    Apply table-specific business rules.

    Generic cleaning belongs in silver_transformer.py.
    Business-specific logic belongs here.
    """

    df = df.copy()

    if table_name == "customers":

        if "email" in df.columns:
            df["email"] = df["email"].str.lower()

        if "state" in df.columns:
            df["state"] = df["state"].str.upper()

    elif table_name == "products":

        if "category" in df.columns:
            df["category"] = df["category"].str.title()

        if "brand" in df.columns:
            df["brand"] = df["brand"].str.title()

    elif table_name == "stores":

        if "state" in df.columns:
            df["state"] = df["state"].str.upper()

        if "region" in df.columns:
            df["region"] = df["region"].str.title()

    elif table_name == "suppliers":

        if "country" in df.columns:
            df["country"] = df["country"].str.title()

    return df