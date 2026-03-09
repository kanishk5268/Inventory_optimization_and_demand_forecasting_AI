from backend.forecasting import forecast_top_product
from backend.inventory_optimizer import calculate_inventory_metrics

forecast, product = forecast_top_product()

print("\nForecast generated for:", product)

inventory = calculate_inventory_metrics()
print(forecast[['ds', 'yhat']].tail())

print("\nInventory Recommendation")

print("Average Daily Demand:", inventory["average_daily_demand"])
print("Safety Stock:", inventory["safety_stock"])
print("Reorder Point:", inventory["reorder_point"])