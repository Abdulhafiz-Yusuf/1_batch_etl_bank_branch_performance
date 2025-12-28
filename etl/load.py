# load.py
from config import DB_CONFIG
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch


def load_data(transformed_data: pd.DataFrame) -> None:
    """
    Load transformed data into the bronze.stg_bank_branch_performance table
    using an idempotent UPSERT strategy.

    - Drops rows violating primary key grain
    - Converts pandas NaT / NaN to PostgreSQL NULL
    """

    # -------------------- SAFETY CHECKS --------------------

    # Enforce PK grain: rows without branch_id or performance_date are invalid
    df = transformed_data.dropna(
        subset=["branch_id", "performance_date"]
    )

    if df.empty:
        print("No valid rows to load after PK validation.")
        return

    # Convert pandas NaT / NaN to Python None → PostgreSQL NULL
    df = df.where(pd.notnull(df), None)
    conn = None
    try:
        # -------------------- CONNECT --------------------
        conn = psycopg2.connect(**DB_CONFIG)

        # -------------------- UPSERT SQL --------------------
        sql = """
            INSERT INTO bronze.bank_branch_performance (
                branch_id,
                branch_name,
                performance_date,
                total_deposits,
                total_loans,
                new_accounts,
                closed_accounts,
                net_profit,
                operating_expenses
            )
            VALUES (
                %(branch_id)s,
                %(branch_name)s,
                %(performance_date)s,
                %(total_deposits)s,
                %(total_loans)s,
                %(new_accounts)s,
                %(closed_accounts)s,
                %(net_profit)s,
                %(operating_expenses)s
            )
            ON CONFLICT (branch_id, performance_date)
            DO UPDATE SET
                branch_name = EXCLUDED.branch_name,
                total_deposits = EXCLUDED.total_deposits,
                total_loans = EXCLUDED.total_loans,
                new_accounts = EXCLUDED.new_accounts,
                closed_accounts = EXCLUDED.closed_accounts,
                net_profit = EXCLUDED.net_profit,
                operating_expenses = EXCLUDED.operating_expenses;
        """

        records = df.to_dict(orient="records")

        # -------------------- EXECUTE --------------------
        with conn.cursor() as cur:
            execute_batch(cur, sql, records, page_size=500)
            conn.commit()
            
        
        print(f"Attempted to load {len(df)} records into bronze.bank_branch_performance.\n")
    

    except Exception as e:
        print(f"Error while loading data: {e}")
        if conn:
            conn.rollback()
        raise

    finally:
        if conn:
            conn.close()
