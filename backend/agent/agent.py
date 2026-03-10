import ollama
from backend.forecasting import forecast_product
from backend.inventory_optimizer import calculate_inventory_metrics
from backend.db import engine
import pandas as pd
from backend.agent.sql_agent import sql_agent
from backend.data_loader import (
    get_top_products,
    demand_by_region,
    demand_by_category,
    sales_by_market
)

def run_forecast_tool(product):

    forecast, product_name = forecast_product(product)

    avg_demand = forecast["yhat"].mean()

    return f"""
Forecast generated for {product_name}.
Average predicted daily demand: {avg_demand:.2f}
"""


def run_inventory_tool(product):

    metrics = calculate_inventory_metrics(product)

    return f"""
Inventory Metrics for {metrics['product']}

Average Daily Demand: {metrics['average_daily_demand']:.2f}
Safety Stock: {metrics['safety_stock']:.2f}
Reorder Point: {metrics['reorder_point']:.2f}
"""


from backend.data_loader import get_top_products


def create_agent(question, product):

    question = question.lower()

    # TOOL 1: Top Products
    if "top" in question and "product" in question:

        df = get_top_products()

        result = "Top 5 Selling Products:\n\n"

        for i, row in df.iterrows():
            result += f"{i+1}. {row['Product Name']} — {row['total_sales']:.0f} total sales\n"

        return result


    # TOOL 2: Category Analytics
    elif "category" in question:

        df = demand_by_category()

        result = "Sales by Category:\n\n"

        for i, row in df.iterrows():
            result += f"{row['Category Name']} — {row['total_sales']:.0f}\n"

        return result


    # TOOL 3: Market Analytics
    elif "market" in question:

        df = sales_by_market()

        result = "Sales by Market:\n\n"

        for i, row in df.iterrows():
            result += f"{row['Market']} — {row['total_sales']:.0f}\n"

        return result


    # TOOL 4: Region Analytics
    elif "region" in question:

        df = demand_by_region()

        result = "Sales by Region:\n\n"

        for i, row in df.iterrows():
            result += f"{row['Order Region']} — {row['total_sales']:.0f}\n"

        return result


    # TOOL 5: Forecast
    elif "forecast" in question:

        forecast, product_name = forecast_product(product)

        avg_demand = forecast["yhat"].mean()

        return f"""
Forecast generated for {product_name}

Average predicted demand: {avg_demand:.2f}
"""


    # TOOL 6: Inventory Optimization
    elif "inventory" in question or "stock" in question:

        metrics = calculate_inventory_metrics(product)

        return f"""
Inventory Metrics for {metrics['product']}

Average Daily Demand: {metrics['average_daily_demand']}
Safety Stock: {metrics['safety_stock']}
Reorder Point: {metrics['reorder_point']}
"""


    # FALLBACK LLM
    else:
     return sql_agent(question)
        # response = ollama.chat(
        #     model="llama3",
        #     messages=[
        #         {
        #             "role": "system",
        #             "content": "You are a supply chain assistant. Only answer based on provided tools and data."
        #         },
        #         {"role": "user", "content": question}
        #     ]
        # )

        # return response["message"]["content"]


# sql execution code

def run_sql_query(query):

    try:

        df = pd.read_sql(query, engine)

        if df.empty:
            return "No data found."

        return df.to_string(index=False)

    except Exception as e:

        return f"SQL Error: {str(e)}"
    

#####################################################################

# #def create_agent(question, product):

#     # Decide tool
#     if "forecast" in question.lower():
#         tool_output = run_forecast_tool(product)

#     elif "inventory" in question.lower() or "stock" in question.lower():
#         tool_output = run_inventory_tool(product)

#     else:
#         tool_output = "I could not determine which analysis to run."

#     # Ask LLM to explain results
#     response = ollama.chat(
#         model="llama3",
#         messages=[
#             {"role": "system", "content": "You are an AI supply chain assistant."},
#             {"role": "user", "content": question},
#             {"role": "assistant", "content": tool_output},
#         ],
#     )

#     return response["message"]["content"]



# # from openai import OpenAI
# # from backend.forecasting import forecast_product
# # from backend.inventory_optimizer import calculate_inventory_metrics
# # from dotenv import load_dotenv
# # import os 

# # load_dotenv()
# # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# # def run_forecast_tool(product):

# #     forecast, product_name = forecast_product(product)

# #     avg_demand = forecast["yhat"].mean()

# #     return f"""
# # Forecast generated for {product_name}.
# # Average predicted daily demand: {avg_demand:.2f}
# # """


# # def run_inventory_tool(product):

# #     metrics = calculate_inventory_metrics(product)

# #     return f"""
# # Inventory Metrics for {metrics['product']}

# # Average Daily Demand: {metrics['average_daily_demand']:.2f}
# # Safety Stock: {metrics['safety_stock']:.2f}
# # Reorder Point: {metrics['reorder_point']:.2f}
# # """


# # def create_agent(question, product):

# #     # Decide which tool to run
# #     if "forecast" in question.lower():
# #         tool_output = run_forecast_tool(product)

# #     elif "inventory" in question.lower() or "stock" in question.lower():
# #         tool_output = run_inventory_tool(product)

# #     else:
# #         tool_output = "I could not determine which analysis to run."

# #     # Send tool result to LLM for explanation
# #     response = client.chat.completions.create(
# #         model="gpt-4o-mini",
# #         messages=[
# #             {"role": "system", "content": "You are a supply chain AI assistant."},
# #             {"role": "user", "content": question},
# #             {"role": "assistant", "content": tool_output},
# #         ],
# #     )

# #     return response.choices[0].message.content



# # # from langchain.tools import tool
# # # from langchain_openai import ChatOpenAI
# # from langchain.agents import initialize_agent, AgentType

# # from backend.forecasting import forecast_product
# # from backend.inventory_optimizer import calculate_inventory_metrics


# # # -------------------------------
# # # Forecast Tool
# # # -------------------------------
# # @tool
# # def forecast_tool(product: str) -> str:
# #     """Generate demand forecast for a product"""

# #     forecast, product_name = forecast_product(product)

# #     avg_demand = forecast["yhat"].mean()

# #     return f"Forecast generated for {product_name}. Average predicted demand: {avg_demand:.2f}"


# # # -------------------------------
# # # Inventory Tool
# # # -------------------------------
# # @tool
# # def inventory_tool(product: str) -> str:
# #     """Calculate inventory metrics for a product"""

# #     metrics = calculate_inventory_metrics(product)

# #     return f"""
# # Product: {metrics['product']}
# # Average Daily Demand: {metrics['average_daily_demand']:.2f}
# # Safety Stock: {metrics['safety_stock']:.2f}
# # Reorder Point: {metrics['reorder_point']:.2f}
# # """


# # # -------------------------------
# # # Create Agent
# # # -------------------------------
# # def create_agent():

# #     llm = ChatOpenAI(
# #         model="gpt-4o-mini",
# #         temperature=0
# #     )

# #     tools = [
# #         forecast_tool,
# #         inventory_tool
# #     ]

# #     agent = initialize_agent(
# #         tools=tools,
# #         llm=llm,
# #         agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
# #         verbose=True
# #     )

# #     return agent