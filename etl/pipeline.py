# pipeline.py
from pathlib import Path
from extract import extract_data 
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
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    run_etl_pipeline(DATA_DIR)