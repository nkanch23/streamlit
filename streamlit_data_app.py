import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on July 14th")
st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

st.bar_chart(df, x="Category", y="Sales")

st.dataframe(df.groupby("Category").sum())

st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)

sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
st.dataframe(sales_by_month)

st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")

selected_category = st.selectbox(
    "Select a Category:",
    options=df["Category"].unique()
)

filtered_subcategories = df[df["Category"] == selected_category]["Sub_Category"].unique()
selected_subcategories = st.multiselect(
    f"Select Sub-Categories from {selected_category}:",
    options=filtered_subcategories,
    default=filtered_subcategories
)

if selected_subcategories:
    filtered_df = df[
        (df["Category"] == selected_category) & 
        (df["Sub_Category"].isin(selected_subcategories))
    ]
    
    sales_by_month_filtered = filtered_df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
    st.line_chart(sales_by_month_filtered, y="Sales")
    
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0
    
    overall_profit_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100
    margin_delta = profit_margin - overall_profit_margin
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Sales",
            value=f"${total_sales:,.2f}"
        )
    
    with col2:
        st.metric(
            label="Total Profit", 
            value=f"${total_profit:,.2f}"
        )
    
    with col3:
        st.metric(
            label="Overall Profit Margin (%)",
            value=f"{profit_margin:.2f}%",
            delta=f"{margin_delta:.2f}%"
        )
else:
    st.write("Please select at least one sub-category to view the analysis.")