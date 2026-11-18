"""
app.py
The dashboard (the part the user sees in the browser).

Run it with:   python -m streamlit run app.py
Streamlit turns this Python file into a web page.
"""

import streamlit as st

from analysis import explain_product, load_data, overall_summary, product_analysis

st.set_page_config(page_title="Business Loss Detective", page_icon="🔍", layout="wide")

st.title("🔍 Business Loss Detective")
st.write(
    "Finds products with unusual cancellation rates and shows how much "
    "sales value is tied to those cancellations, so you know what to investigate first."
)

# ---- Load the data -------------------------------------------------------
df = load_data("business_data.csv")

# ---- Sidebar: settings the user can change ------------------------------
st.sidebar.header("Settings")
min_orders = st.sidebar.slider("Minimum orders to judge a product", 1, 100, 10)
margin = st.sidebar.slider("Flag if cancellation rate is this many points above average", 0, 20, 5)

# ---- Top numbers (KPIs) --------------------------------------------------
summary = overall_summary(df)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total orders", summary["total_orders"])
c2.metric("Cancellation rate", f"{summary['cancellation_rate']:.1f}%")
c3.metric("Return rate", f"{summary['return_rate']:.1f}%")
c4.metric("Revenue", f"Rs {summary['revenue']:,.0f}")
c5.metric("Profit", f"Rs {summary['profit']:,.0f}")

# ---- Product table -------------------------------------------------------
table = product_analysis(df, min_orders=min_orders, margin=margin)

st.subheader("Cancellation rate by product")
st.bar_chart(table["Cancellation Rate"])

st.subheader("Product analysis")
st.dataframe(table.round(1), use_container_width=True)

# ---- Investigation list --------------------------------------------------
st.subheader("Products that need investigation")
flagged = table[table["Needs Investigation"]].sort_values("Priority Rank")

if flagged.empty:
    st.success("No product is unusually high right now.")
else:
    for product, row in flagged.iterrows():
        info = explain_product(product, row, summary["cancellation_rate"])
        with st.expander(f"#{int(row['Priority Rank'])}  {product}", expanded=True):
            st.markdown("**What the data shows (facts):**")
            for line in info["evidence"]:
                st.write("- " + line)
            st.markdown("**Possible reasons (NOT proven, someone must check):**")
            for line in info["unverified"]:
                st.write("- " + line)
