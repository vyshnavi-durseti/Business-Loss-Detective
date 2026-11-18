"""
generate_data.py
Creates fake (synthetic) order data and saves it as business_data.csv.

We do not have a real shop, so we invent 1000 orders.
We deliberately make the Webcam cancel more often (25% instead of 10%)
so that we can test whether our analysis can find that hidden problem.
"""

import random
from datetime import datetime, timedelta

import pandas as pd

# A "seed" makes the random numbers repeat, so every run gives the same data.
random.seed(42)

# product name: (selling price, cost price)
products = {
    "Laptop": (50000, 42000),
    "Mouse": (1000, 600),
    "Keyboard": (3000, 2000),
    "Headphones": (4000, 2500),
    "Monitor": (15000, 12000),
    "Webcam": (5000, 3500),
    "SSD": (7000, 5000),
}

rows = []
start_date = datetime(2026, 9, 1)

for i in range(1000):
    product = random.choice(list(products.keys()))
    price, cost = products[product]

    # Status chances: [Completed, Cancelled, Returned] in percent
    if product == "Webcam":
        weights = [70, 25, 5]   # the planted problem: 25% cancelled
    else:
        weights = [85, 10, 5]   # normal: 10% cancelled
    status = random.choices(["Completed", "Cancelled", "Returned"], weights=weights)[0]

    # Planted clue: cancelled Webcam orders were slow to process (5-10 days).
    if product == "Webcam" and status == "Cancelled":
        processing_days = random.randint(5, 10)
    else:
        processing_days = random.randint(1, 10)

    order_date = start_date + timedelta(days=random.randint(0, 59))

    rows.append({
        "Order_ID": 1001 + i,
        "Product": product,
        "Price": price,
        "Cost": cost,
        "Status": status,
        "Processing_Days": processing_days,
        "Date": order_date.strftime("%Y-%m-%d"),
    })

df = pd.DataFrame(rows)
df.to_csv("business_data.csv", index=False)

print("Created business_data.csv")
print("Total orders:", len(df))
