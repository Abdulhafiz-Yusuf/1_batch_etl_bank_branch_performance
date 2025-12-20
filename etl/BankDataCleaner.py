import pandas as pd
import numpy as np
import re

class BankDataCleaner:
    """
    A reusable class to clean banking datasets (customers, accounts, transactions)
    with automatic data quality reporting (KPI) for ETL workflows.
    """

    def __init__(self):
        self.cleaning_rules = {
            'text_columns': self.clean_text,
            'email_columns': self.clean_email,
            'phone_columns': self.clean_phone,
            'account_columns': self.clean_account_number,
            'transaction_columns': self.clean_transaction_id,
            'date_columns': self.clean_dates,
            'numeric_columns': self.clean_numeric
        }

    # ------------------- Cleaning Methods -------------------
    def clean_text(self, series):
        return (series.astype(str)
                .str.strip()
                .str.upper()
                .replace(['NAN', 'NONE', ''], np.nan)
                .fillna('UNKNOWN'))

    def clean_email(self, series):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        cleaned = series.astype(str).str.lower().str.strip()
        return cleaned.where(cleaned.str.match(email_pattern), np.nan)

    def clean_phone(self, series):
        return (series.astype(str)
                .str.replace(r'[^\d]', '', regex=True)
                .replace('', np.nan))

    def clean_account_number(self, series):
        return (series.astype(str)
                .str.strip()
                .str.upper()
                .where(series.astype(str).str.match(r'^\d{10,12}$'), np.nan))

    def clean_transaction_id(self, series):
        return (series.astype(str)
                .str.strip()
                .str.upper()
                .replace(['NAN', 'NONE', ''], np.nan))

    def clean_dates(self, series):
        return pd.to_datetime(series, errors='coerce')

    def clean_numeric(self, series):
        return pd.to_numeric(series, errors='coerce')

    # ------------------- Main Cleaner -------------------
    def clean_dataframe(self, df, column_types, generate_kpi=True):
        """
        Clean a dataframe based on column types.
        Optionally generate KPI summary for data quality.
        """
        df_clean = df.copy()

        for col_type, columns in column_types.items():
            if col_type in self.cleaning_rules:
                for col in columns:
                    if col in df_clean.columns:
                        df_clean[col] = self.cleaning_rules[col_type](df_clean[col])

        if generate_kpi:
            kpi = self.generate_kpi(df_clean)
            return df_clean, kpi
        return df_clean

    # ------------------- KPI / Data Quality -------------------
    def generate_kpi(self, df):
        """
        Generate data quality metrics for each column:
        - Total missing values
        - % missing
        - Basic stats for numeric columns
        """
        kpi = pd.DataFrame(columns=['column', 'dtype', 'missing', 'missing_pct', 'unique', 'min', 'max', 'mean'])

        for col in df.columns:
            dtype = df[col].dtype
            missing = df[col].isna().sum()
            missing_pct = round((missing / len(df)) * 100, 2)
            unique = df[col].nunique(dropna=True)
            min_val = df[col].min() if np.issubdtype(dtype, np.number) else None
            max_val = df[col].max() if np.issubdtype(dtype, np.number) else None
            mean_val = df[col].mean() if np.issubdtype(dtype, np.number) else None

            kpi = kpi.append({
                'column': col,
                'dtype': dtype,
                'missing': missing,
                'missing_pct': missing_pct,
                'unique': unique,
                'min': min_val,
                'max': max_val,
                'mean': mean_val
            }, ignore_index=True)

        return kpi
