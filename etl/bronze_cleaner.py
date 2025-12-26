import pandas as pd
from typing import Dict, List, Tuple


class BronzeCleaner:
    """
    Bronze-layer cleaner:
    - Enforces schema
    - Parses dates
    - Coerces numerics
    - Performs minimal normalization
    - Tracks cleaning impact (KPIs)
    - Leaves business meaning untouched
    """

    # -------------------- BASIC CLEANERS --------------------

    @staticmethod
    def clean_dates(series: pd.Series) -> pd.Series:
        return pd.to_datetime(series, errors="coerce")

    @staticmethod
    def clean_numeric(series: pd.Series) -> pd.Series:
        return pd.to_numeric(series, errors="coerce")

    @staticmethod
    def clean_text(series: pd.Series) -> pd.Series:
        return (
            series.astype(str)
            .str.strip()
            .replace(
                {
                    "": None,
                    "NAN": None,
                    "NONE": None,
                    "nan": None,
                    "None": None,
                }
            )
        )

    # -------------------- MAIN ORCHESTRATOR --------------------

    def clean_dataframe(
        self,
        df: pd.DataFrame,
        column_types: Dict[str, List[str]],
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Clean dataframe based on declared column groups.

        Returns:
            cleaned_df (pd.DataFrame)
            kpi_df (pd.DataFrame) -> cleaning impact metrics
        """

        df_clean = df.copy()
        kpi_data = []

        # ---------- TEXT COLUMNS ----------
        for col in column_types.get("text_columns", []):
            if col in df_clean.columns:
                before = df_clean[col].notna().sum()
                df_clean[col] = self.clean_text(df_clean[col])
                after = df_clean[col].notna().sum()

                kpi_data.append(
                    {
                        "column": col,
                        "data_type": "text",
                        "nulls_introduced_due_to_cleaning": before - after,
                        "cleaning_method": "strip_and_basic_null_normalization",
                    }
                )

        # ---------- DATE COLUMNS ----------
        for col in column_types.get("date_columns", []):
            if col in df_clean.columns:
                before = df_clean[col].notna().sum()
                df_clean[col] = self.clean_dates(df_clean[col])
                after = df_clean[col].notna().sum()

                kpi_data.append(
                    {
                        "column": col,
                        "data_type": "date",
                        "nulls_introduced_due_to_cleaning": before - after,
                        "cleaning_method": "datetime_coercion",
                    }
                )

        # ---------- NUMERIC COLUMNS ----------
        for col in column_types.get("numeric_columns", []):
            if col in df_clean.columns:
                before = df_clean[col].notna().sum()
                df_clean[col] = self.clean_numeric(df_clean[col])
                after = df_clean[col].notna().sum()

                kpi_data.append(
                    {
                        "column": col,
                        "data_type": "numeric",
                        "nulls_introduced_due_to_cleaning": before - after,
                        "cleaning_method": "numeric_type_coercion",
                    }
                )

        kpi_df = pd.DataFrame(kpi_data)

        return df_clean, kpi_df
