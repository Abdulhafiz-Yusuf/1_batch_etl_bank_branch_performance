# transform

import pandas as pd

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        from bank_data_cleaner import BankDataCleaner
        cleaner = BankDataCleaner()
        branch_column_types = {
            'text_columns': ['branch_id','branch_name'],
            'date_columns': ['date'],
            'numeric_columns': [
                'new_accounts',
                'operating_expenses',
                'net_profit',
                'closed_accounts',
                'total_loans',
                'total_deposits'
            ]
        }

        cleaned_df, kpi_df = cleaner.clean_dataframe(df, branch_column_types)

        # optional: persist KPI later
        print("\n📊 Data Quality KPI Summary. \n")
        print(kpi_df)
        print(f"\n{cleaned_df.shape[0]} rows transformed successfully.\n")
        return cleaned_df

    except Exception as e:
        print(f"An error occurred while transforming data: {e}")
        return pd.DataFrame()
