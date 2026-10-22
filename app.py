import pandas as pd

df = pd.read_csv("business_data.csv")

print("Total orders:", len(df))
print(df.head())
total_orders = len(df)

cancelled_orders = (df["Status"] == "Cancelled").sum()

cancellation_rate = (cancelled_orders / total_orders) * 100

print("Total orders:", total_orders)
print("Cancelled orders:", cancelled_orders)
print("Cancellation rate:", cancellation_rate, "%")
completed = df[df["Status"] == "Completed"]

revenue = completed["Price"].sum()
profit = (completed["Price"] - completed["Cost"]).sum()

print("Revenue:", revenue)
print("Profit:", profit)
orders_by_product = df.groupby("Product").size()

print("Orders by product:")
print(orders_by_product)
cancelled_by_product = (
    df[df["Status"] == "Cancelled"]
    .groupby("Product")
    .size()
)

print("Cancelled orders by product:")
print(cancelled_by_product)
cancellation_rate_by_product = (
    cancelled_by_product / orders_by_product * 100
)

print("Cancellation rate by product:")
print(cancellation_rate_by_product)
product_analysis = pd.DataFrame({
    "Total Orders": orders_by_product,
    "Cancelled Orders": cancelled_by_product
}).fillna(0)

product_analysis["Cancellation Rate"] = (
    product_analysis["Cancelled Orders"]
    / product_analysis["Total Orders"]
    * 100
)

minimum_orders = 10

product_analysis["Needs Investigation"] = (
    (product_analysis["Total Orders"] >= minimum_orders)
    & (product_analysis["Cancellation Rate"] > cancellation_rate)
)

print("Product Analysis:")
print(product_analysis)
cancelled_order_value = (
    df[df["Status"] == "Cancelled"]
    .groupby("Product")["Price"]
    .sum()
)

product_analysis["Cancelled Order Value"] = (
    cancelled_order_value
)

product_analysis = product_analysis.fillna(0)

print("Product Analysis with Financial Impact:")
print(product_analysis)