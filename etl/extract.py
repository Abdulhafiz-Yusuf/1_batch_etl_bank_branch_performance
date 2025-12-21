import pandas as pd

def extract_data(file_path: str) -> pd.DataFrame:
    """
    Extract data from a CSV file and return it as a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: The extracted data as a DataFrame.
    """
    try:
        # Read the raw csv file
        data = pd.read_csv(file_path, dtype={"branch_id": str})
        print("\n\nData extraction completed successfully.")
        return data
    except Exception as e:
        print(f"An error occurred while extracting data: {e}")
        return pd.DataFrame()
if __name__ == "__main__":
    import os
    df = extract_data(os.path.join('data','bank_branch_performance.csv'))
    null_branch = df[df['branch_name'].isnull()]
    
    # print(null_branch['branch_id',])
    # print(df.query('branch_name.isnull()')
    #     #   [['branch_id', 'date', 'net_profit']]
    #       )
    # print(df.isna().sum())
    print(df.info())
    # df.dtypes
    # df.shape
