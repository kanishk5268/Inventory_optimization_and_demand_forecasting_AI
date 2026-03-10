import streamlit as st
import pandas as pd
import sys
import os
import matplotlib.pyplot as plt

## Add project root to python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from backend.inventory_optimizer import detect_inventory_risk , generate_supply_chain_insights
from backend.forecasting import forecast_top_products, forecast_product
from backend.data_loader import (
    get_all_products,
    get_top_products,
    demand_by_region,
    demand_by_category,
    sales_by_market,
    late_delivery_analysis,
    sales_by_customer_segment
)
from backend.agent.agent import create_agent






st.set_page_config(page_title="Inventory Optimization Dashboard", layout="wide")

st.title("AI Inventory Optimization Dashboard")

if "forecast" not in st.session_state:
    st.session_state["forecast"] = None

if "metrics" not in st.session_state:
    st.session_state["metrics"] = None

products = get_all_products()

selected_product = st.selectbox(
    "Select Product",
    products
)

forecast = st.session_state.get("forecast")
metrics = st.session_state.get("metrics")
if st.button("Run Forecast"):

    forecast, product, metrics = forecast_product(selected_product)

    #metrics = calculate_inventory_metrics(selected_product)

    st.session_state["forecast"] = forecast
    st.session_state["metrics"] = metrics
    
    st.subheader("Inventory Metrics")

    st.write("Average Daily Demand:", round(metrics["average_daily_demand"],2))
    st.write("Safety Stock:", round(metrics["safety_stock"],2))
    st.write("Reorder Point:", round(metrics["reorder_point"],2))

    st.subheader("Demand Forecast")

    fig, ax = plt.subplots(figsize=(12,6))

    ax.plot(forecast["ds"], forecast["yhat"], label="Forecast")

    ax.fill_between(
        forecast["ds"],
        forecast["yhat_lower"],
        forecast["yhat_upper"],
        alpha=0.3
    )

    ax.legend()

    st.pyplot(fig)

st.header("AI Supply Chain Assistant")

question = st.text_input("Ask a question")


if st.button("Ask AI"):

    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        response = create_agent(question, selected_product)
        st.write(response)

    # Retrieve stored forecast and metrics
    forecast = st.session_state.get("forecast")
    metrics = st.session_state.get("metrics")

    # Demand Trend
    if forecast is not None:

        st.subheader("Demand Trend")

        trend = forecast[['ds','yhat']].set_index('ds')

        st.line_chart(trend)

    # Inventory Risk
    if metrics is not None:

        st.subheader("Inventory Risk")

        risk = detect_inventory_risk(metrics)

        st.warning(risk)



st.header("Top Selling Products")
top_products = get_top_products()
st.dataframe(top_products)
st.bar_chart(top_products.set_index("Product Name")["total_sales"])

## regional analytics
region_sales = demand_by_region()
st.bar_chart(region_sales.set_index("Order Region"))

## displaying mae and rmse

if metrics is not None: 
    st.subheader("Forecast Accuracy")

    col1, col2, col3 = st.columns(3)

    col1.metric("MAE", round(metrics["MAE"],2))
    col2.metric("RMSE", round(metrics["RMSE"],2))
    col3.metric("MAPE (%)", round(metrics["MAPE"],2))

    st.subheader("Supply Chain Risk")

    risk = detect_inventory_risk(metrics)

    st.warning(risk)
    st.subheader("AI Supply Chain Advisor")

    insights = generate_supply_chain_insights(
        selected_product,
        metrics,
        forecast
    )

    st.info(insights)


# Demand by Category
st.header("Demand by Category")

category_sales = demand_by_category()

st.bar_chart(category_sales.set_index("Category Name")["total_sales"])

#Sales by Market
st.header("Sales by Market")

market_sales = sales_by_market()

st.bar_chart(market_sales.set_index("Market")["total_sales"])


# Delivery Performance
st.header("Delivery Performance")

delivery_status = late_delivery_analysis()

st.bar_chart(delivery_status.set_index("Delivery Status")["total_orders"])

# Customer Segment Sales

st.header("Customer Segment Sales")

segment_sales = sales_by_customer_segment()

st.bar_chart(segment_sales.set_index("Customer Segment")["total_sales"])


st.header("Multi-Product Forecast")

multi_forecast = forecast_top_products()

st.dataframe(multi_forecast)

st.bar_chart(multi_forecast.set_index("Product")["Forecast Demand"])