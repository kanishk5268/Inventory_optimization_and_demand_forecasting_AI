import numpy as np
from backend.forecasting import forecast_top_product


def calculate_inventory_metrics(product_name):

    # Get forecast for top selling product
    forecast, product_name = forecast_top_product()

    # Use predicted demand (yhat)
    demand = forecast['yhat']

    # Average daily demand
    avg_demand = demand.mean()

    # Demand standard deviation
    demand_std = demand.std()

    # Assumptions (can be tuned later)
    lead_time = 7        # days
    service_level = 1.65 # 95% service level

    # Safety Stock
    safety_stock = service_level * demand_std * np.sqrt(lead_time)

    # Reorder Point
    reorder_point = (avg_demand * lead_time) + safety_stock

    # Optimal Inventory Level
    optimal_inventory = reorder_point + (avg_demand * lead_time)

    return {
        "product": product_name,
        "average_daily_demand": round(avg_demand,2),
        "safety_stock": round(safety_stock,2),
        "reorder_point": round(reorder_point,2),
        "optimal_inventory": round(optimal_inventory,2)
    }

