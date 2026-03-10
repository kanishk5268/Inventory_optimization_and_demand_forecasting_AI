import pandas as pd
from sqlalchemy import create_engine
from .db import engine

# get salesdata

def load_sales_data():
    query = """
    SELECT *
    FROM supplychain_data
    """
    
    df = pd.read_sql(query, engine)
    
    return df

# get top selling product

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

# get product sales (product_name)

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

# get all products

def get_all_products():

    query = """
    SELECT DISTINCT "Product Name" 
    FROM supplychain_data
    ORDER BY "Product Name"
    """
    
    df = pd.read_sql(query, engine)

    return df["Product Name"].tolist()

# get top products limited = 5

def get_top_products(limit=5):

    query = f"""
    SELECT "Product Name", SUM("Sales") AS total_sales
    FROM supplychain_data
    GROUP BY "Product Name"
    ORDER BY total_sales DESC
    LIMIT {limit}
    """

    df = pd.read_sql(query, engine)

    return df

# demand by region

def demand_by_region():
    query = """
    SELECT "Order Region", SUM("Sales") as total_sales
    FROM supplychain_data
    GROUP BY "Order Region"
    ORDER BY total_sales DESC
    """

    return pd.read_sql(query, engine) 

# demand by category

def demand_by_category():

    query = """
    SELECT "Category Name", SUM("Sales") as total_sales
    FROM supplychain_data
    GROUP BY "Category Name"
    ORDER BY total_sales DESC
    """

    df = pd.read_sql(query, engine)

    return df

# sales by market

def sales_by_market():

    query = """
    SELECT "Market", SUM("Sales") as total_sales
    FROM supplychain_data
    GROUP BY "Market"
    ORDER BY total_sales DESC
    """

    df = pd.read_sql(query, engine)

    return df

# late delivery risk
def late_delivery_analysis():

    query = """
    SELECT "Delivery Status", COUNT(*) as total_orders
    FROM supplychain_data
    GROUP BY "Delivery Status"
    """

    df = pd.read_sql(query, engine)

    return df

# customer segment sales
def sales_by_customer_segment():

    query = """
    SELECT "Customer Segment", SUM("Sales") as total_sales
    FROM supplychain_data
    GROUP BY "Customer Segment"
    ORDER BY total_sales DESC
    """

    df = pd.read_sql(query, engine)

    return df
