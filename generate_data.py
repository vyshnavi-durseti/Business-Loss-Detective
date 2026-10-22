import pandas as pd
import random
from datetime import datetime, timedelta

products = {
    "Laptop": (50000, 42000),
    "Mouse": (1000, 600),
    "Keyboard": (3000, 2000),
    "Headphones": (4000, 2500),
    "Monitor": (15000, 12000),
    "Webcam": (5000, 3500),
    "SSD": (7000, 5000)
}

rows = []

start_date = datetime(2026, 9, 1)

for i in range(1000):
    product = random.choice(list(products.keys()))

    price, cost = products[product]

    if product == "Webcam":
     status = random.choices(
        ["Completed", "Cancelled", "Returned"],
        weights=[70, 25, 5]
    )[0]
    else:
     status = random.choices(
        ["Completed", "Cancelled", "Returned"],
        weights=[85, 10, 5]
    )[0]

    processing_days = random.randint(1, 10)

    order_date = start_date + timedelta(days=random.randint(0, 59))

    rows.append({
        "Order_ID": 1001 + i,
        "Product": product,
        "Price": price,
        "Cost": cost,
        "Status": status,
        "Processing_Days": processing_days,
        "Date": order_date.strftime("%Y-%m-%d")
    })

df = pd.DataFrame(rows)

df.to_csv("business_data.csv", index=False)

print("Created business_data.csv")
print("Total orders:", len(df))