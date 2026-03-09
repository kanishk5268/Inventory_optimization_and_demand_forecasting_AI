import streamlit as st
import pandas as pd
import sys
import os
import matplotlib.pyplot as plt

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from backend.inventory_optimizer import calculate_inventory_metrics
from backend.forecasting import forecast_top_product
from backend.forecasting import forecast_product
from backend.data_loader import get_all_products
from backend.agent.agent import create_agent

st.set_page_config(page_title="Inventory Optimization Dashboard", layout="wide")

st.title("AI Inventory Optimization Dashboard")

products = get_all_products()

selected_product = st.selectbox(
    "Select Product",
    products
)

if st.button("Run Forecast"):

    forecast, product = forecast_product(selected_product)

    metrics = calculate_inventory_metrics(selected_product)

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

from backend.agent.agent import create_agent

st.header("AI Supply Chain Assistant")

question = st.text_input("Ask a question")

if st.button("Ask AI"):

    response = create_agent(question, selected_product)

    st.write(response)
#############################################################################

# st.title("📦 AI Inventory Optimization & Demand Forecasting")

# # Get forecast and metrics
# forecast, product = forecast_top_product()
# metrics = calculate_inventory_metrics()

# # --- Product Info ---
# st.subheader("Top Selling Product")
# st.write(product)

# # --- Inventory Metrics ---
# st.subheader("Inventory Metrics")

# col1, col2, col3, col4 = st.columns(4)

# col1.metric("Average Daily Demand", round(metrics["average_daily_demand"],2))
# col2.metric("Safety Stock", round(metrics["safety_stock"],2))
# col3.metric("Reorder Point", round(metrics["reorder_point"],2))
# col4.metric("Optimal Inventory", round(metrics["optimal_inventory"],2))

# # --- Forecast Chart ---
# st.subheader("Demand Forecast")

# forecast_chart = forecast[['ds','yhat']].set_index('ds')

# st.line_chart(forecast_chart)




#########################################
# import streamlit as st
# import sys
# import os
# import matplotlib.pyplot as plt

# sys.path.append(os.path.abspath("../backend"))

# from inventory_optimizer import calculate_inventory_metrics
# from forecasting import forecast_top_product


# st.title("Inventory Optimization & Demand Forecasting Dashboard")

# # Button to run analysis
# if st.button("Run Forecast & Inventory Optimization"):

#     forecast, product = forecast_top_product()
#     metrics = calculate_inventory_metrics()

#     st.subheader("Top Product")
#     st.write(product)

#     st.subheader("Inventory Metrics")

#     st.write("Average Daily Demand:", round(metrics["average_daily_demand"],2))
#     st.write("Safety Stock:", round(metrics["safety_stock"],2))
#     st.write("Reorder Point:", round(metrics["reorder_point"],2))
#     st.write("Optimal Inventory:", round(metrics["optimal_inventory"],2))


#     st.subheader("Demand Forecast")

#     fig, ax = plt.subplots(figsize=(12,6))

#     ax.plot(forecast['ds'], forecast['yhat'], label="Forecast")
#     ax.fill_between(
#         forecast['ds'],
#         forecast['yhat_lower'],
#         forecast['yhat_upper'],
#         alpha=0.3
#     )

#     ax.set_title(f"Demand Forecast for {product}")
#     ax.legend()

#     st.pyplot(fig)