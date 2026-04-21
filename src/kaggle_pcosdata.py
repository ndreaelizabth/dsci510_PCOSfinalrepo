import pandas as pd

def load_pcos_data(file_path="data/pcos_dataset.csv"):
    """
    Load the PCOS dataset from a CSV file.

    Args:
        file_path (str): Path to the CSV file

    Returns:
        pd.DataFrame: Loaded dataset
    """
    df = pd.read_csv(file_path)
    return df


if __name__ == "__main__":
    df = load_pcos_data()
    print("Dataset loaded successfully.")
    print(f"Shape: {df.shape}")
    print("\nFirst 5 rows:")
    print(df.head())