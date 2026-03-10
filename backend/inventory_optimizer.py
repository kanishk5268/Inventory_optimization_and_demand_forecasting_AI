import numpy as np
from backend.forecasting import forecast_product
#from backend.forecasting import forecast_top_product


def calculate_inventory_metrics(forecast, product_name):

    demand = forecast["yhat"]

    avg_demand = demand.mean()
    demand_std = demand.std()

    lead_time = 7
    service_level = 1.65

    safety_stock = service_level * demand_std * np.sqrt(lead_time)

    reorder_point = (avg_demand * lead_time) + safety_stock

    optimal_inventory = reorder_point + (avg_demand * lead_time)

    return {
        "product": product_name,
        "average_daily_demand": round(avg_demand,2),
        "safety_stock": round(safety_stock,2),
        "reorder_point": round(reorder_point,2),
        "optimal_inventory": round(optimal_inventory,2)
    }

def detect_inventory_risk(metrics):

    if metrics["optimal_inventory"] < metrics["reorder_point"]:
        return "⚠️ Risk of stockout"

    if metrics["optimal_inventory"] > metrics["reorder_point"] * 2:
        return "⚠️ Overstock risk"

    return "Inventory levels healthy"

def detect_inventory_risk(metrics):

    demand = metrics["average_daily_demand"]
    reorder = metrics["reorder_point"]

    if demand > reorder:

        return "⚠ High Stockout Risk — Demand exceeds reorder level"

    elif demand < reorder * 0.5:

        return "⚠ Overstock Risk — Inventory too high"

    else:

        return "✅ Inventory Level Normal"


def generate_supply_chain_insights(product, metrics, forecast):

    avg_demand = metrics["average_daily_demand"]
    safety_stock = metrics["safety_stock"]
    reorder_point = metrics["reorder_point"]

    future_demand = forecast["yhat"].tail(30).mean()

    insight = f"""
Supply Chain Insight Report for {product}

Forecast Analysis
The predicted average demand over the next period is approximately {future_demand:.2f} units per day.

Inventory Policy
Current safety stock level is {safety_stock:.2f} units.

Reorder Strategy
The reorder point is set at {reorder_point:.2f} units.

Recommendation
"""

    if future_demand > avg_demand * 1.2:

        insight += """
Demand is expected to increase significantly. Consider increasing safety stock to avoid stockouts.
"""

    elif future_demand < avg_demand * 0.8:

        insight += """
Demand appears to be declining. Consider reducing inventory levels to avoid overstocking.
"""

    else:

        insight += """
Demand appears stable. Current inventory strategy is appropriate.
"""

    return insight


