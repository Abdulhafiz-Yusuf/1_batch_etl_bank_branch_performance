import pandas as pd

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform the input DataFrame by cleaning and normalizing the data.

    Parameters:
    df (pd.DataFrame): The input DataFrame to be transformed.

    Returns:
    pd.DataFrame: The transformed DataFrame.
    """
    try:
        from etl.BankDataCleaner import BankDataCleaner
        cleaner = BankDataCleaner()

        branch_column_types={
            'text_columns': ['branch_id', 'branch_name', ],
            # 'email_columns': ['email'],
            # 'phone_columns': ['phone'],
            # 'account_columns': ['account_number'],
            'date_columns': ['date'],
            'numeric_columns': ['new_accounts',
                                'operating_expenses', 
                                'net_profit', 
                                'closed_accounts',
                                'total_loans',
                                'total_deposits']
        }

        cleaned_df = cleaner.clean_dataframe(df, branch_column_types)   
        return cleaned_df
    except Exception as e:
        print(f"An error occurred while transforming data: {e}")
        return pd.DataFrame()
    