import pandas as pd

def load_pcos_data(file_path="data/PCOS_data.csv"):
    df = pd.read_csv(file_path)
    return df


if __name__ == "__main__":
    df = load_pcos_data()
    print("Dataset loaded successfully.")
    print(f"Shape: {df.shape}")
    print(df.head())