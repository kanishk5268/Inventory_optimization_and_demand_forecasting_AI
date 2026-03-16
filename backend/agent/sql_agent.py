import ollama
from backend.agent.sql_tool import execute_sql


def generate_sql(question):

    prompt = f"""
You are a supply chain data analyst.

Convert the question into a PostgreSQL SQL query.

Table: supplychain_data

Columns:
"Product Name"
"Sales"
"Category Name"
"Market"
"Order Region"
"Customer Segment"
"Delivery Status"

Rules:
1. Always wrap column names in DOUBLE QUOTES.
2. Column names contain spaces.
3. Return ONLY the SQL query.
4. Do NOT include explanations.
5. Do NOT include markdown.

Question: {question}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    sql_query = response["message"]["content"]

    # remove markdown
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    # keep only SQL part
    if "SELECT" in sql_query:
        sql_query = sql_query[sql_query.index("SELECT"):]

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