from backend.inventory_optimizer import calculate_inventory_metrics

metrics = calculate_inventory_metrics()

print("\nInventory Optimization Results")
print("--------------------------------")
print("Product:", metrics["product"])
print("Average Daily Demand:", metrics["average_daily_demand"])
print("Safety Stock:", metrics["safety_stock"])
print("Reorder Point:", metrics["reorder_point"])
print("Optimal Inventory:", metrics["optimal_inventory"])