# pipeline.py
import os
from extract import extract_data  # Direct import, no "etl."
from transform import transform_data
from load import load_data


def run_etl_pipeline(file_path: str) -> None:
    """
    Run the ETL pipeline: Extract, Transform, Load.

    Parameters:
    file_path (str): The path to the input CSV file.
    """
    # Extract
    raw_data = extract_data(file_path)
    if raw_data.empty:
        print("No data extracted. Exiting ETL pipeline.")
        return

    # Transform
    transformed_data = transform_data(raw_data)
    if transformed_data.empty:
        print("No data transformed. Exiting ETL pipeline.")
        return

    # Load
    load_data(transformed_data)
    print("ETL pipeline completed successfully.\n")

if __name__ == "__main__":
    raw_data_file_path = os.path.join("..","data", "bank_branch_performance.csv")
    run_etl_pipeline(raw_data_file_path)