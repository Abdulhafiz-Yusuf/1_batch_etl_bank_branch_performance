import pandas as pd
from sqlalchemy import create_engine, text

def load_data(transformed_data: pd.DataFrame) -> None:
    """
    Load transformed data into the silver.bank_branch_performance table.
    Safely refreshes the table without dropping dependent views.
    """
    df = transformed_data
    try:
        # 1. Connect to the database
        engine = create_engine("postgresql://abuammar:abuammar123@localhost:5432/de_db")

        with engine.begin() as conn:
            result = conn.execute(text(
                "SELECT to_regclass('silver.bank_branch_performance')"
            )).scalar()
            
            if result:
                conn.execute(text("DELETE FROM silver.bank_branch_performance"))

            # 3. Load the transformed data
            df.to_sql(
                "bank_branch_performance",
                engine,
                schema="silver",
                if_exists="append",  # append to truncated table
                index=False
            )

        rows = df.shape[0]
        print(f"{rows} rows loaded to silver.bank_branch_performance successfully.\n")

    except Exception as e:
        print(f"An error occurred while loading data: {e}")
