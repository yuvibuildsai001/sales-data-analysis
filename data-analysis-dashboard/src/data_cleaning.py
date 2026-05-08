"""
data_cleaning.py
----------------
Loads raw sales data, performs cleaning & feature engineering,
and saves the processed file to data/processed/.
"""

import pandas as pd
import os


def load_raw_data(filepath: str = "data/raw/sales_data.csv") -> pd.DataFrame:
    """Load the raw CSV into a DataFrame."""
    df = pd.read_csv(filepath)
    print(f"📥  Loaded  {len(df)} rows  ×  {len(df.columns)} columns  from  {filepath}")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform all cleaning steps:
      1. Drop duplicate rows
      2. Handle missing values
      3. Fix data types
      4. Feature engineering (month, quarter, day_of_week)
    """
    original_rows = len(df)

    # ── 1. Remove duplicates ───────────────────────────────────────────────────
    df = df.drop_duplicates()
    print(f"🗑️   Removed {original_rows - len(df)} duplicate rows")

    # ── 2. Handle missing values ───────────────────────────────────────────────
    missing_before = df.isnull().sum().sum()

    # Fill missing unit_price with the median price of the same category
    df["unit_price"] = df.groupby("category")["unit_price"].transform(
        lambda x: x.fillna(x.median())
    )
    # Recalculate total_amount for rows where it was missing
    df["total_amount"] = df["total_amount"].fillna(df["unit_price"] * df["quantity"])

    missing_after = df.isnull().sum().sum()
    print(f"🩹  Fixed {missing_before - missing_after} missing values")

    # ── 3. Fix data types ──────────────────────────────────────────────────────
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["unit_price"] = df["unit_price"].round(2)
    df["total_amount"] = df["total_amount"].round(2)

    # ── 4. Feature engineering ─────────────────────────────────────────────────
    df["month"]        = df["order_date"].dt.month
    df["month_name"]   = df["order_date"].dt.strftime("%b")
    df["quarter"]      = df["order_date"].dt.quarter.map({1: "Q1", 2: "Q2", 3: "Q3", 4: "Q4"})
    df["day_of_week"]  = df["order_date"].dt.day_name()
    df["is_weekend"]   = df["day_of_week"].isin(["Saturday", "Sunday"])

    print(f"✅  Cleaning complete  →  {len(df)} clean rows remaining")
    return df


def save_clean_data(df: pd.DataFrame, filepath: str = "data/processed/sales_clean.csv") -> None:
    """Save the cleaned DataFrame to CSV."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"💾  Saved clean data  →  {filepath}")


def run_cleaning_pipeline() -> pd.DataFrame:
    """End-to-end cleaning pipeline."""
    df = load_raw_data()
    df = clean_data(df)
    save_clean_data(df)
    return df


if __name__ == "__main__":
    run_cleaning_pipeline()
