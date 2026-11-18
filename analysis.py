"""
analysis.py
All the "thinking" of the project lives here.
app.py (the dashboard) only calls these functions and shows the results.
"""

import pandas as pd


def load_data(path="business_data.csv"):
    """Read the CSV file into a table (DataFrame)."""
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])
    return df


def overall_summary(df):
    """Numbers for the whole business."""
    total = len(df)
    cancelled = int((df["Status"] == "Cancelled").sum())
    returned = int((df["Status"] == "Returned").sum())

    # Revenue and profit are counted only from Completed orders.
    completed = df[df["Status"] == "Completed"]
    revenue = completed["Price"].sum()
    profit = (completed["Price"] - completed["Cost"]).sum()

    return {
        "total_orders": total,
        "cancelled_orders": cancelled,
        "returned_orders": returned,
        "cancellation_rate": cancelled / total * 100,
        "return_rate": returned / total * 100,
        "revenue": revenue,
        "profit": profit,
    }


def product_analysis(df, min_orders=10, margin=5.0):
    """
    One row per product with counts, rates and money.

    A product is flagged "Needs Investigation" only when BOTH are true:
      1. It has at least `min_orders` orders (so tiny samples do not fool us).
      2. Its cancellation rate is more than `margin` percentage points
         above the overall cancellation rate (so normal random ups and
         downs do not get flagged).
    """
    overall_rate = (df["Status"] == "Cancelled").mean() * 100

    cancelled = df[df["Status"] == "Cancelled"]
    returned = df[df["Status"] == "Returned"]
    completed = df[df["Status"] == "Completed"]

    table = pd.DataFrame({
        "Total Orders": df.groupby("Product").size(),
        "Cancelled Orders": cancelled.groupby("Product").size(),
        "Returned Orders": returned.groupby("Product").size(),
        "Cancelled Value": cancelled.groupby("Product")["Price"].sum(),
    })
    # A product with zero cancellations has no row in `cancelled`, so fill 0.
    table = table.fillna(0)

    table["Cancellation Rate"] = table["Cancelled Orders"] / table["Total Orders"] * 100
    table["Return Rate"] = table["Returned Orders"] / table["Total Orders"] * 100

    table["Avg Days (Cancelled)"] = cancelled.groupby("Product")["Processing_Days"].mean()
    table["Avg Days (Completed)"] = completed.groupby("Product")["Processing_Days"].mean()

    table["Needs Investigation"] = (
        (table["Total Orders"] >= min_orders)
        & (table["Cancellation Rate"] > overall_rate + margin)
    )

    # Priority: among flagged products, biggest cancelled value = rank 1.
    flagged_value = table["Cancelled Value"].where(table["Needs Investigation"])
    table["Priority Rank"] = flagged_value.rank(ascending=False, method="min")

    return table.sort_values("Cancelled Value", ascending=False)


def explain_product(product, row, overall_rate):
    """
    Build a simple explanation for one product.
    It is split in two parts on purpose:
      - evidence: facts that come directly from the data
      - unverified: ideas that could explain the facts, but the data
        cannot prove them (someone must check them in real life).
    """
    evidence = [
        f"{product} has {int(row['Total Orders'])} orders, and "
        f"{int(row['Cancelled Orders'])} were cancelled "
        f"({row['Cancellation Rate']:.1f}%).",
        f"The overall cancellation rate is {overall_rate:.1f}%.",
        f"Cancelled {product} orders add up to Rs {row['Cancelled Value']:,.0f} "
        f"of sales value that did not happen.",
    ]

    unverified = [
        "The product may have a quality problem or wrong description.",
        "The price may be higher than what customers expect.",
        "Stock or delivery problems may make customers give up.",
    ]

    days_cancelled = row["Avg Days (Cancelled)"]
    days_completed = row["Avg Days (Completed)"]
    if pd.notna(days_cancelled) and pd.notna(days_completed):
        if days_cancelled - days_completed >= 1:
            evidence.append(
                f"Cancelled orders took {days_cancelled:.1f} days to process, "
                f"but completed orders took {days_completed:.1f} days."
            )
            unverified.insert(
                0,
                "Slow processing may be making customers cancel. "
                "(The data shows the two go together, not that one causes the other.)",
            )

    return {"evidence": evidence, "unverified": unverified}
