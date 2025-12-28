import pandas as pd
from pathlib import Path

def extract_data(file_path: str) -> pd.DataFrame:
    """
    Reads all CSV files in a folder and returns
    a single concatenated DataFrame.
    """
    try:
        folder_path = Path(file_path)
        csv_files = list(folder_path.glob("*.csv"))

        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in {folder_path}")

        dataframes = []

        for file in csv_files:
            print(f"📥 Reading {file.name}")
            df = pd.read_csv(file)
            dataframes.append(df)

        combined_df = pd.concat(dataframes, ignore_index=True)

        print(f"✅ Extracted {len(combined_df)} total rows from {len(csv_files)} files")

        return combined_df

    except Exception as e:
        print(f"An error occurred while extracting data: {e}")
        return pd.DataFrame()




if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    df = extract_data(DATA_DIR)
    # null_branch = df[df['branch_name'].isnull()]
    # print(df.query('branch_name.isnull()')
    # print(df.isna().sum())
    print(df.info())
    # df.dtypes
    # df.shape
