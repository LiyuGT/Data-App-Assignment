import streamlit as st
import pandas as pd

st.title("Data App Assignment")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
category = st.selectbox("Select Category", df['Category'].unique())

st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
sub_categories = st.multiselect("Select Sub-Category", df[df['Category'] == category]['Sub_Category'].unique())

st.write("### (3) show a line chart of sales for the selected items in (2)")
def filter_data(category, sub_categories):
    filtered_df = df[(df['Category'] == category) & (df['Sub_Category'].isin(sub_categories))]
    return filtered_df

filtered_df = filter_data(category, sub_categories)
st.dataframe(filtered_df)  

# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month2 = filtered_df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
st.dataframe(sales_by_month2)
# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month2, y="Sales")

st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
if not filtered_df.empty:
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    overall_profit_margin = (total_profit / total_sales) * 100

    st.metric(label="Total Sales", value=f"${total_sales:.2f}")
    st.metric(label="Total Profit", value=f"${total_profit:.2f}")
    st.metric(label="Overall Profit Margin (%)", value=f"{overall_profit_margin:.2f}%")



st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
if not filtered_df.empty:
    overall_avg_profit_margin = (df['Profit'].sum() / df['Sales'].sum()) * 100
    delta_margin = overall_profit_margin - overall_avg_profit_margin
    st.metric(label="Overall Profit Margin vs Average", value=f"{delta_margin:.2f}%", delta=delta_margin)
