import os
import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

user = os.getenv("DB_USER")
password = quote_plus(os.getenv("DB_PASSWORD"))
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")

DB_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(DB_URL)

def load_dataset():

    df = pd.read_csv(
        "../data/DataCoSupplyChainDataset.csv",
        encoding="ISO-8859-1"
    )

    df.to_sql(
        "supplychain_data",
        engine,
        if_exists="replace",
        index=False
    )

    print("Dataset loaded into database successfully!")


if __name__ == "__main__":
    load_dataset()