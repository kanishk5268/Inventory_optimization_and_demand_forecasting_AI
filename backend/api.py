from fastapi import FastAPI
from inventory_optimizer import calculate_inventory_metrics

app = FastAPI(title="Inventory Optimization API")

@app.get("/")
def home():
    return {"message": "Inventory Optimization API is running"}

@app.get("/inventory-metrics")
def get_inventory_metrics():

    metrics = calculate_inventory_metrics()

    return {
        "product": metrics["product"],
        "average_daily_demand": round(metrics["average_daily_demand"], 2),
        "safety_stock": round(metrics["safety_stock"], 2),
        "reorder_point": round(metrics["reorder_point"], 2),
        "optimal_inventory": round(metrics["optimal_inventory"], 2)
    }