import streamlit as st
import pandas as pd

st.title("Data App Assignment – Due July 14")

# Load data
df = pd.read_csv("Superstore_Sales_utf8.csv")

st.write("### Full Dataset")
st.dataframe(df)

# Initial bar charts
st.bar_chart(df, x="Category", y="Sales")
st.dataframe(df.groupby("Category").sum())
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Time-based analysis — use a separate copy
df_time = df.copy()
df_time["Order_Date"] = pd.to_datetime(df_time["Order_Date"])
df_time.set_index("Order_Date", inplace=True)

# Monthly sales (all data)
sales_by_month = df_time.filter(items=["Sales"]).groupby(pd.Grouper(freq='ME')).sum()
st.write("### Monthly Sales (All Categories)")
st.dataframe(sales_by_month)
st.line_chart(sales_by_month, y="Sales")

# -----------------------
# Your Additions Section
# -----------------------
st.header("Your Additions")

# (1) Dropdown for Category
category = st.selectbox("Select a Category", df["Category"].unique())

# (2) Multi-select for Sub-Category (within selected category)
filtered_df = df[df["Category"] == category]
subcategories = filtered_df["Sub_Category"].unique()
selected_subcats = st.multiselect("Select Sub-Categories", subcategories, default=list(subcategories))

# Filter based on selection
selected_df = filtered_df[filtered_df["Sub_Category"].isin(selected_subcats)]

# (3) Line chart of Sales over time for selected items
if not selected_df.empty:
    df_selected_time = selected_df.copy()
    df_selected_time["Order_Date"] = pd.to_datetime(df_selected_time["Order_Date"])
    df_selected_time.set_index("Order_Date", inplace=True)

    sales_by_month_filtered = df_selected_time.groupby(pd.Grouper(freq='ME'))['Sales'].sum()
    st.write(f"### Monthly Sales for Selected Sub-Categories in {category}")
    st.line_chart(sales_by_month_filtered)

    # (4) Metrics for selected items
    total_sales = selected_df["Sales"].sum()
    total_profit = selected_df["Profit"].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

    # (5) Delta: Compare with overall profit margin
    overall_sales = df["Sales"].sum()
    overall_profit = df["Profit"].sum()
    overall_margin = (overall_profit / overall_sales) * 100 if overall_sales != 0 else 0
    delta_margin = round(profit_margin - overall_margin, 2)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Profit Margin (%)", f"{profit_margin:.2f}%", delta=f"{delta_margin:+.2f}%")

else:
    st.warning("No data available for selected sub-categories.")
