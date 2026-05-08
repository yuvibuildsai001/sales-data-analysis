"""
generate_data.py
----------------
Generates a realistic synthetic Indian e-commerce sales dataset (1000 records).
Run this first before anything else.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os


def generate_sales_data(n_records: int = 1000, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)
    random.seed(seed)

    # ── Geography ──────────────────────────────────────────────────────────────
    cities_states = {
        "Mumbai": "Maharashtra",
        "Pune": "Maharashtra",
        "Nagpur": "Maharashtra",
        "Delhi": "Delhi",
        "Noida": "Uttar Pradesh",
        "Gurgaon": "Haryana",
        "Bengaluru": "Karnataka",
        "Mysuru": "Karnataka",
        "Chennai": "Tamil Nadu",
        "Coimbatore": "Tamil Nadu",
        "Hyderabad": "Telangana",
        "Kolkata": "West Bengal",
        "Ahmedabad": "Gujarat",
        "Surat": "Gujarat",
        "Jaipur": "Rajasthan",
    }

    # ── Products ───────────────────────────────────────────────────────────────
    categories_products = {
        "Electronics":    ["Smartphone", "Laptop", "Headphones", "Smart TV", "Tablet", "Smartwatch"],
        "Clothing":       ["T-Shirt", "Jeans", "Kurta", "Saree", "Jacket", "Sneakers"],
        "Home & Kitchen": ["Mixer Grinder", "Pressure Cooker", "Bedsheet", "Curtains", "Air Purifier"],
        "Books":          ["Engineering Textbook", "Fiction Novel", "Self-Help Book", "UPSC Guide", "Python Programming"],
        "Sports":         ["Cricket Bat", "Badminton Racket", "Yoga Mat", "Dumbbells", "Running Shoes"],
        "Grocery":        ["Basmati Rice", "Toor Dal", "Cooking Oil", "Spice Set", "Tea Powder"],
    }

    price_ranges = {
        "Electronics":    (500,  80_000),
        "Clothing":       (200,   5_000),
        "Home & Kitchen": (300,  15_000),
        "Books":          (100,     800),
        "Sports":         (300,  10_000),
        "Grocery":        ( 50,     500),
    }

    # ── Payment ────────────────────────────────────────────────────────────────
    payment_methods = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash on Delivery", "EMI"]
    payment_weights = [0.35,         0.20,          0.18,          0.10,              0.12,       0.05]

    start_date = datetime(2024, 1, 1)

    records = []
    for i in range(1, n_records + 1):
        city     = random.choice(list(cities_states.keys()))
        state    = cities_states[city]
        category = random.choice(list(categories_products.keys()))
        product  = random.choice(categories_products[category])

        lo, hi     = price_ranges[category]
        unit_price = round(random.uniform(lo, hi), 2)
        quantity   = random.choices([1, 2, 3, 4, 5], weights=[0.50, 0.25, 0.12, 0.08, 0.05])[0]
        total      = round(unit_price * quantity, 2)

        # Introduce ~3 % missing values to make cleaning realistic
        if random.random() < 0.03:
            unit_price = None
            total      = None

        order_date = start_date + timedelta(days=random.randint(0, 364))
        payment    = random.choices(payment_methods, weights=payment_weights)[0]
        rating     = round(random.uniform(2.5, 5.0), 1)

        records.append({
            "order_id":       f"ORD{i:05d}",
            "order_date":     order_date.strftime("%Y-%m-%d"),
            "customer_city":  city,
            "customer_state": state,
            "category":       category,
            "product_name":   product,
            "quantity":       quantity,
            "unit_price":     unit_price,
            "total_amount":   total,
            "payment_method": payment,
            "rating":         rating,
        })

    df = pd.DataFrame(records)

    # Add ~1 % duplicate rows to simulate real-world messy data
    dup_idx = np.random.choice(len(df), size=10, replace=False)
    df = pd.concat([df, df.iloc[dup_idx]], ignore_index=True)

    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/sales_data.csv", index=False)
    print(f"✅  Dataset generated  →  data/raw/sales_data.csv  ({len(df)} rows)")
    return df


if __name__ == "__main__":
    generate_sales_data()
