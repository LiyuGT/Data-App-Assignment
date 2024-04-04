import streamlit as st
import pandas as pd

st.title("Data App Assignment")

st.write("### Input Data")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)


# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)

st.write("## Additions")
st.write("### (1) Drop down for Category")
category = st.selectbox("Select Category", df['Category'].unique())

st.write("### (2) Multi-select for Sub_Category *in the selected Category*")
sub_categories = st.multiselect("Select Sub-Category", df[df['Category'] == category]['Sub_Category'].unique())

st.write("### (3) Line chart of sales for the selected items")
def filter_data(category, sub_categories):
    filtered_df = df[(df['Category'] == category) & (df['Sub_Category'].isin(sub_categories))]
    return filtered_df

filtered_df = filter_data(category, sub_categories)
st.dataframe(filtered_df)  

# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month2 = filtered_df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
# st.dataframe(sales_by_month2)
# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month2, y="Sales")

st.write("### (4) Metrics: total sales, total profit, and overall profit margin")
if not filtered_df.empty:
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    overall_profit_margin = (total_profit / total_sales) * 100

    st.metric(label="Total Sales", value=f"${total_sales:.2f}")
    st.metric(label="Total Profit", value=f"${total_profit:.2f}")
    st.metric(label="Overall Profit Margin (%)", value=f"{overall_profit_margin:.2f}%")



st.write("### (5) Overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
if not filtered_df.empty:
    overall_avg_profit_margin = (df['Profit'].sum() / df['Sales'].sum()) * 100
    delta_margin = overall_profit_margin - overall_avg_profit_margin
    st.metric(label="Overall Profit Margin vs Average", value=f"{delta_margin:.2f}%", delta=delta_margin)
