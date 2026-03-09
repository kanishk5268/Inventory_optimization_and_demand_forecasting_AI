#import pandas as pd
#from prophet import Prophet
import os
from .data_loader import get_top_selling_product, get_product_sales
import pandas as pd
from prophet import Prophet


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

    return forecast, product_name

#def forecast_product(product_name):

    print("Product:", product_name)

    # Load product sales
    daily_sales = get_product_sales(product_name)

    print("Incoming Columns:", daily_sales.columns)

    # Rename columns for Prophet
    prophet_df = daily_sales.rename(
        columns={
            "order_date": "ds",
            "sales": "y"
        }
    )

    # Ensure datetime format
    prophet_df["ds"] = pd.to_datetime(prophet_df["ds"])

    # -------------------------------
    # Load holidays file safely
    # -------------------------------
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    holiday_path = os.path.join(BASE_DIR, "data", "puertorican_holidays.csv")

    holidays = pd.read_csv(holiday_path)

    holidays = holidays.rename(
        columns={
            "Date": "ds",
            "Name": "holiday"
        }
    )

    holidays["ds"] = pd.to_datetime(holidays["ds"])

    # Prophet expects only these columns
    holidays = holidays[["ds", "holiday"]]

    # -------------------------------
    # Train Prophet model
    # -------------------------------
    model = Prophet(holidays=holidays)

    model.fit(prophet_df)

    # Forecast next 365 days
    future = model.make_future_dataframe(periods=365)

    forecast = model.predict(future)

    return forecast, product_name


#def forecast_product(product_name):

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

    holidays = pd.read_csv( r"D:\Inventory_Optimization_and_Demand_forecasting\data\puertorican_holidays.csv")
    # BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # holiday_path = os.path.join(BASE_DIR, "data", "puertorican_holidays.csv")

    # holidays = pd.read_csv(holiday_path)

    


    holidays = holidays.rename(
        columns={
            "Date": "ds",
            "Name": "holiday"
        }
    )

    holidays["ds"] = pd.to_datetime(holidays["ds"])

    model = Prophet(holidays=holidays)

    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=365)

    forecast = model.predict(future)

    return forecast, product_name