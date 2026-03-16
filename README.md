# AI Inventory Optimization & Demand Forecasting

An AI-powered supply chain analytics system that forecasts product demand and optimizes inventory levels using machine learning and data analytics.

The system analyzes historical sales data to predict future demand and recommend optimal inventory policies such as safety stock and reorder points.

---

# Project Overview

Modern supply chains require accurate demand forecasting and efficient inventory management to avoid stockouts and overstock situations.

This project uses **time series forecasting, data analytics, and AI agents** to provide intelligent supply chain insights and inventory recommendations.

The system includes:

- Demand forecasting using Facebook Prophet
- Inventory optimization models
- SQL-based data analytics
- AI supply chain assistant
- Interactive dashboard for visualization

---

# Features

Demand Forecasting  
Predicts future demand using Prophet time-series forecasting.

Inventory Optimization  
Calculates:

- Average daily demand
- Safety stock
- Reorder point
- Optimal inventory levels

AI Supply Chain Assistant  
Users can ask natural language questions like:

- Top selling products
- Sales by region
- Category demand
- Market performance
- Inventory recommendations

Interactive Dashboard  
A Streamlit dashboard visualizes:

- Forecast trends
- Inventory metrics
- Supply chain insights
- Sales analytics

API Support  
FastAPI endpoint for retrieving inventory metrics.

---

# Tech Stack

Python  
Pandas  
Scikit-learn  
Facebook Prophet  
PostgreSQL  
SQLAlchemy  
FastAPI  
Streamlit  
Ollama LLM (Llama3)

---

# Project Architecture

### System Architecture

                        ┌───────────────────────────────┐
                        │        User Interface         │
                        │        (Streamlit App)        │
                        │           app.py              │
                        └──────────────┬────────────────┘
                                       │
                                       │ User Queries / Dashboard Interaction
                                       ▼
                        ┌───────────────────────────────┐
                        │        AI Agent Layer         │
                        │          agent.py             │
                        │  Natural Language Interface   │
                        └──────────────┬────────────────┘
                                       │
                     ┌─────────────────┼──────────────────┐
                     │                 │                  │
                     ▼                 ▼                  ▼
          ┌────────────────┐  ┌──────────────────┐  ┌─────────────────┐
          │ SQL AI Agent   │  │ Forecast Engine  │  │ Inventory Engine│
          │ sql_agent.py   │  │ forecasting.py   │  │ inventory_opt.py│
          └────────┬───────┘  └────────┬─────────┘  └─────────┬───────┘
                   │                   │                      │
                   ▼                   ▼                      ▼
          ┌─────────────────────────────────────────────────────────┐
          │                    Data Analytics Layer                 │
          │                     data_loader.py                      │
          │    Sales analytics, region demand, category analysis    │
          └──────────────────────────┬──────────────────────────────┘
                                     │
                                     ▼
                          ┌────────────────────┐
                          │    Database Layer  │
                          │   PostgreSQL DB    │
                          │ supplychain_data   │
                          └─────────┬──────────┘
                                    │
                                    ▼
                          ┌────────────────────┐
                          │ Data Loader Script │
                          │       db.py        │
                          │ CSV → PostgreSQL   │
                          └────────────────────┘


                        External AI Model
                ┌───────────────────┐
                │  Ollama LLM       │
                │  (Llama3 Model)   │
                └───────────────────┘

### Workflow



                           User Prompt
                                ↓
                        Agent interprets prompt
                                ↓
                    Agent calls forecasting tool
                                ↓
                    Tool queries database
                                ↓
                    Forecast model runs
                                ↓
                    Agent summarizes result
                                ↓
                    Streamlit displays answer + chart

# Dataset

The project uses the **DataCo Supply Chain Dataset** containing:

- Product Name
- Sales
- Category
- Market
- Order Region
- Customer Segment
- Delivery Status
- Order Dates

The dataset is loaded into PostgreSQL for analytics and forecasting.

---

# Forecasting Model

Demand forecasting uses **Facebook Prophet**, a time-series forecasting library designed for business data.

The model predicts future product demand using historical sales data and holiday effects.

Example:


forecast = model.predict(future)


The system also evaluates model accuracy using:

- MAE
- RMSE
- MAPE

---

# Inventory Optimization

Inventory metrics are calculated based on forecast demand:

Safety Stock


        Safety Stock = Z × σ × √Lead Time


Reorder Point


        Reorder Point = (Average Demand × Lead Time) + Safety Stock


Optimal Inventory


        Optimal Inventory = Reorder Point + Lead Time Demand


These calculations are implemented in the inventory optimization module.

---

# AI Agent

The system includes an AI agent that routes user questions to different analytics tools.

Example capabilities:

- Top selling products
- Demand by category
- Sales by region
- Market analysis
- Demand forecasting
- Inventory recommendations

The agent dynamically selects the appropriate tool based on the user query. 

---

# API

A FastAPI service provides inventory recommendations.

Example endpoint:


        GET /inventory-metrics


Returns:


        {
        "product": "...",
        "average_daily_demand": ...,
        "safety_stock": ...,
        "reorder_point": ...,
        "optimal_inventory": ...
        }


API implemented using FastAPI.

---

# Running the Project

1. Install dependencies


        pip install -r requirements.txt


2. Load dataset into PostgreSQL


        python backend/db.py


3. Run Streamlit dashboard


        streamlit run frontend/app.py


4. Start FastAPI server


        uvicorn api:app --reload


---

# Example Dashboard Features

- Forecast demand trends
- Inventory risk alerts
- Supply chain insights
- Sales analytics by region, category, and market
- Multi-product demand forecasting

Dashboard implementation using Streamlit.

---

# Future Improvements

- Deep learning demand forecasting (LSTM / Transformers)
- Real-time inventory monitoring
- Automated replenishment recommendations
- Multi-warehouse optimization
- Reinforcement learning for supply chain decisions

---
