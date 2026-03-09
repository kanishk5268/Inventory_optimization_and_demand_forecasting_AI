import pandas as pd
from sqlalchemy import create_engine
from .db import engine

def load_sales_data():
    query = """
    SELECT *
    FROM supplychain_data
    """
    
    df = pd.read_sql(query, engine)
    
    return df


def get_top_selling_product():

    query = """
    SELECT "Product Name", SUM("Sales") as total_sales
    FROM supplychain_data
    GROUP BY "Product Name"
    ORDER BY total_sales DESC
    LIMIT 1
    """

    df = pd.read_sql(query, engine)

    return df.iloc[0]["Product Name"]

def get_product_sales(product_name):

    query = """
    SELECT
        "order date (DateOrders)" as order_date,
        SUM("Sales") as sales
    FROM supplychain_data
    WHERE "Product Name" = %s
    GROUP BY order_date
    ORDER BY order_date
    """

    df = pd.read_sql(query, engine, params=(product_name,))
    df["order_date"] = pd.to_datetime(df["order_date"])

    return df

def get_all_products():

    query = """
    SELECT DISTINCT "Product Name" 
    FROM supplychain_data
    ORDER BY "Product Name"
    """
    
    df = pd.read_sql(query, engine)

    return df["Product Name"].tolist()