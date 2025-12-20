# import pandas as pd

# def transform_data(df: pd.DataFrame) -> pd.DataFrame:
#     """
#     Transform the input DataFrame by cleaning and normalizing the data.

#     Parameters:
#     df (pd.DataFrame): The input DataFrame to be transformed.

#     Returns:
#     pd.DataFrame: The transformed DataFrame.
#     """
#     try:
#        # Return early on empty input
#         if df.empty:
#             return df

#         # Remove duplicates and work on a copy
#         df_clean = df.drop_duplicates().copy()

#         # Parse a date column if present
#         if 'date' in df_clean.columns:
#             df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce')

#         # Ensure numeric columns are numeric
#         numeric_cols = ['closed_accounts', 'net_profit', 'operating_expenses']
#         for col in numeric_cols:
#             if col in df_clean.columns:
#                 df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

#         return df_clean
#     except Exception as e:
#         print(f"An error occurred while transforming data: {e}")
#         return pd.DataFrame()
    
