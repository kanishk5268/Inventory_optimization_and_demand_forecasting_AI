import ollama
from backend.forecasting import forecast_product
from backend.inventory_optimizer import calculate_inventory_metrics


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


def create_agent(question, product):

    # Decide tool
    if "forecast" in question.lower():
        tool_output = run_forecast_tool(product)

    elif "inventory" in question.lower() or "stock" in question.lower():
        tool_output = run_inventory_tool(product)

    else:
        tool_output = "I could not determine which analysis to run."

    # Ask LLM to explain results
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": "You are an AI supply chain assistant."},
            {"role": "user", "content": question},
            {"role": "assistant", "content": tool_output},
        ],
    )

    return response["message"]["content"]



















# from openai import OpenAI
# from backend.forecasting import forecast_product
# from backend.inventory_optimizer import calculate_inventory_metrics
# from dotenv import load_dotenv
# import os 

# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# def run_forecast_tool(product):

#     forecast, product_name = forecast_product(product)

#     avg_demand = forecast["yhat"].mean()

#     return f"""
# Forecast generated for {product_name}.
# Average predicted daily demand: {avg_demand:.2f}
# """


# def run_inventory_tool(product):

#     metrics = calculate_inventory_metrics(product)

#     return f"""
# Inventory Metrics for {metrics['product']}

# Average Daily Demand: {metrics['average_daily_demand']:.2f}
# Safety Stock: {metrics['safety_stock']:.2f}
# Reorder Point: {metrics['reorder_point']:.2f}
# """


# def create_agent(question, product):

#     # Decide which tool to run
#     if "forecast" in question.lower():
#         tool_output = run_forecast_tool(product)

#     elif "inventory" in question.lower() or "stock" in question.lower():
#         tool_output = run_inventory_tool(product)

#     else:
#         tool_output = "I could not determine which analysis to run."

#     # Send tool result to LLM for explanation
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "You are a supply chain AI assistant."},
#             {"role": "user", "content": question},
#             {"role": "assistant", "content": tool_output},
#         ],
#     )

#     return response.choices[0].message.content
















# # from langchain.tools import tool
# # from langchain_openai import ChatOpenAI
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