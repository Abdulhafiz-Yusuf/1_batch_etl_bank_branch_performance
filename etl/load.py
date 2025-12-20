import pandas as pd
from sqlalchemy import create_engine

def load_data(transformed_data: pd.DataFrame) -> None:
    df = transformed_data
    try:
    # This function will load data to the destination
    # Implementation goes here:
        # 1. Connect to the database or data warehouse
        engine = create_engine("postgresql://halimat:halimat123@localhost:5432/odoo_db")
  
        # 2. Load the transformed data into the appropriate table or collection
        df.to_sql(
        "stg_branch_performance",
        engine,
        schema="staging",
        if_exists="replace",
        index=False)
        return
    except Exception as e:
        print(f"An error occurred while loading data: {e}")
        return
    