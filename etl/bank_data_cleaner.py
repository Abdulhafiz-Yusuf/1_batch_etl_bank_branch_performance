# bank_data_cleaner.py

import pandas as pd
import numpy as np
import re


class BankDataCleaner:
    """
    Reusable cleaner for banking datasets (branches, customers, accounts, transactions)
    with built-in Data Quality KPI generation.
    Compatible with pandas >= 2.0.
    """

    def __init__(self):
        self.cleaning_rules = {
            "text_columns": self.clean_text,
            "email_columns": self.clean_email,
            "phone_columns": self.clean_phone,
            "account_columns": self.clean_account_number,
            "transaction_columns": self.clean_transaction_id,
            "date_columns": self.clean_dates,
            "numeric_columns": self.clean_numeric,
        }

    # -------------------- CLEANING METHODS --------------------

    def clean_text(self, series: pd.Series) -> pd.Series:
        return (
            series.astype(str)
            .str.strip()
            .str.upper()
            .replace(["NAN", "NONE", ""], np.nan)
            .fillna("UNKNOWN")
        )

    def clean_email(self, series: pd.Series) -> pd.Series:
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        cleaned = series.astype(str).str.lower().str.strip()
        return cleaned.where(cleaned.str.match(email_pattern), np.nan)

    def clean_phone(self, series: pd.Series) -> pd.Series:
        return (
            series.astype(str)
            .str.replace(r"[^\d]", "", regex=True)
            .replace("", np.nan)
        )

    def clean_account_number(self, series: pd.Series) -> pd.Series:
        cleaned = series.astype(str).str.strip()
        return cleaned.where(cleaned.str.match(r"^\d{10,12}$"), np.nan)

    def clean_transaction_id(self, series: pd.Series) -> pd.Series:
        return (
            series.astype(str)
            .str.strip()
            .str.upper()
            .replace(["NAN", "NONE", ""], np.nan)
        )

    def clean_dates(self, series: pd.Series) -> pd.Series:
        cleaned = pd.to_datetime(series, errors="coerce")
        return cleaned
    

    def clean_numeric(self, series: pd.Series) -> pd.Series:
        numeric = pd.to_numeric(series, errors="coerce")
        numeric = numeric.fillna(0)
        numeric = numeric.where(numeric >= 0, 0)
        return numeric

    # -------------------- MAIN CLEANER --------------------

    def clean_dataframe(
        self,
        df: pd.DataFrame,
        column_types: dict,
        generate_kpi: bool = True,
    ):
        """
        Clean dataframe based on declared column types.

        Returns:
            cleaned_df (pd.DataFrame)
            kpi_df (pd.DataFrame)  -> only if generate_kpi=True
        """

        df_clean = df.copy()

        for col_type, columns in column_types.items():
            cleaner_func = self.cleaning_rules.get(col_type)

            if not cleaner_func:
                continue

            for col in columns:
                if col in df_clean.columns:
                    df_clean[col] = cleaner_func(df_clean[col])

        if generate_kpi:
            kpi_df = self.generate_kpi(df_clean)
            return df_clean, kpi_df

        return df_clean

    # -------------------- DATA QUALITY KPI --------------------

    def generate_kpi(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate column-level data quality metrics:
        - missing count
        - missing %
        - unique count
        - min / max / mean for numeric columns
        """

        rows = []

        total_rows = len(df)

        for col in df.columns:
            dtype = df[col].dtype
            missing = df[col].isna().sum()
            missing_pct = round((missing / total_rows) * 100, 2) if total_rows else 0
            unique = df[col].nunique(dropna=True)

            is_numeric = np.issubdtype(dtype, np.number)

            rows.append(
                {
                    "column": col,
                    "dtype": str(dtype),
                    "missing": missing,
                    "missing_pct": missing_pct,
                    "unique": unique,
                    "min": df[col].min() if is_numeric else None,
                    "max": df[col].max() if is_numeric else None,
                    "mean": round(df[col].mean(), 2) if is_numeric else None,
                }
            )

        return pd.DataFrame(rows)
