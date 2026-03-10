#import pandas as pd
#from prophet import Prophet
import os
from .data_loader import get_top_selling_product, get_product_sales,get_top_products
import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np


def run_prophet_forecast(df):

    import pandas as pd
    from prophet import Prophet

    print("Incoming Columns:", df.columns)

    # Rename columns dynamically
    if 'order_date' in df.columns:
        prophet_df = df.rename(columns={'order_date': 'ds', 'sales': 'y'})

    elif 'date' in df.columns:
        prophet_df = df.rename(columns={'date': 'ds', 'sales': 'y'})

    elif 'shipping date (DateOrders)' in df.columns:
        prophet_df = df.rename(columns={
            'shipping date (DateOrders)': 'ds',
            'sales': 'y'
        })

    else:
        raise ValueError(f"Unknown date column: {df.columns}")

    # Convert to datetime
    prophet_df['ds'] = pd.to_datetime(prophet_df['ds'])

    # Load holidays
    holidays_df = pd.read_csv(
        r"D:\Inventory_Optimization_and_Demand_forecasting\data\puertorican_holidays.csv"
    )

    holidays_df = holidays_df.rename(columns={
        'Date': 'ds',
        'Name': 'holiday'
    })

    holidays_df['ds'] = pd.to_datetime(holidays_df['ds'])
    holidays_df = holidays_df[['ds', 'holiday']]

    # Prophet model
    model = Prophet(holidays=holidays_df)

    model.fit(prophet_df)

    # Forecast next 24 months
    future = model.make_future_dataframe(periods=730)

    forecast = model.predict(future)

    return forecast


def forecast_top_product():

    # Get top selling product
    product = get_top_selling_product()

    print("Top Product:", product)

    # Get sales data for that product
    daily_sales = get_product_sales(product)

    # Run Prophet forecast
    forecast = run_prophet_forecast(daily_sales)

    return forecast, product

def forecast_product(product_name):

    print("Product:", product_name)

    daily_sales = get_product_sales(product_name)

    print("Incoming Columns:", daily_sales.columns)

    prophet_df = daily_sales.rename(
        columns={
            "order_date": "ds",
            "sales": "y"
        }
    )

    prophet_df["ds"] = pd.to_datetime(prophet_df["ds"])

    # -----------------------------
    # Robust holiday file loading
    # -----------------------------
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    holiday_path = os.path.join(base_dir, "data", "puertorican_holidays.csv")

    print("Holiday file path:", holiday_path)

    if not os.path.exists(holiday_path):
        raise FileNotFoundError(f"Holiday file not found at: {holiday_path}")

    holidays = pd.read_csv(holiday_path)

    holidays = holidays.rename(
        columns={
            "Date": "ds",
            "Name": "holiday"
        }
    )

    holidays["ds"] = pd.to_datetime(holidays["ds"])

    holidays = holidays[["ds", "holiday"]]

    # -----------------------------
    # Train Prophet
    # -----------------------------
    model = Prophet(holidays=holidays)

    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=365)

    forecast = model.predict(future)

    # Evaluate forecast using historical data
    actual = prophet_df["y"]
    predicted = forecast["yhat"][:len(actual)]

    metrics = evaluate_forecast(actual, predicted)

    return forecast, product_name, metrics



def forecast_multiple_products(n=10):

    top_products = get_top_products(n)

    forecasts = {}

    for _, row in top_products.iterrows():

        product = row["Product Name"]

        forecast, _, _ = forecast_product(product)

        forecasts[product] = forecast

    return forecasts



def evaluate_forecast(actual, forecast):

    actual = actual.reset_index(drop=True)
    forecast = forecast.reset_index(drop=True)

    mae = mean_absolute_error(actual, forecast)

    rmse = np.sqrt(mean_squared_error(actual, forecast))

    mape = np.mean(np.abs((actual - forecast) / actual)) * 100

    return {
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape
    }


def forecast_top_products(n=5):

    products = get_top_products(n)

    results = []

    for product in products["Product Name"]:

        forecast, _, metrics = forecast_product(product)

        avg_demand = forecast["yhat"].mean()

        results.append({
            "Product": product,
            "Forecast Demand": avg_demand,
            "MAPE": metrics["MAPE"]
        })

    return pd.DataFrame(results)
