import ollama
from backend.agent.sql_tool import execute_sql


def generate_sql(question):

    prompt = f"""
You are a supply chain data analyst.

Convert the following question into a PostgreSQL SQL query.

Database table: supplychain_data

Columns include:
Product Name
Sales
Category Name
Market
Order Region
Customer Segment
Delivery Status

Return ONLY the SQL query.

Question: {question}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    sql_query = response["message"]["content"]

    return sql_query


def sql_agent(question):

    sql_query = generate_sql(question)

    result = execute_sql(sql_query)

    return f"""
Generated SQL:
{sql_query}

Query Result:
{result}
"""