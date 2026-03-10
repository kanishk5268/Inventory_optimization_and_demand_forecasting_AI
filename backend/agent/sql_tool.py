import pandas as pd
from backend.db import engine


def execute_sql(query):

    try:

        df = pd.read_sql(query, engine)

        if df.empty:
            return "No data found."

        return df.to_string(index=False)

    except Exception as e:

        return f"SQL Error: {str(e)}"