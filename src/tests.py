# AI generated: portions of this file were created with assistance of ChatGPT

import os
import pandas as pd

from config import DATA_DIR, PCOS_DATA_FILE, SYMPTOM_COLUMNS
from kaggle_pcosdata import load_pcos_data, calculate_symptom_percentages


def test_load_pcos_data():
    # Check if the dataset exists before trying to load it
    data_path = os.path.join("..", DATA_DIR, PCOS_DATA_FILE)

    if not os.path.exists(data_path):
        print("Skipping data load test because PCOS_data.csv is not in the data folder.")
        return

    df = load_pcos_data()

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0

    for column in SYMPTOM_COLUMNS:
        assert column in df.columns

    print("test_load_pcos_data passed")


def test_calculate_symptom_percentages():
    # Small fake dataset used only for testing
    sample_data = pd.DataFrame({
        "Cycle(R/I)": [2, 4, 4],
        "Cycle length(days)": [28, 35, 40],
        "Weight gain(Y/N)": [1, 0, 1],
        "hair growth(Y/N)": [0, 1, 1],
        "Skin darkening (Y/N)": [1, 0, 1],
        "Hair loss(Y/N)": [0, 1, 0],
        "Pimples(Y/N)": [1, 1, 0],
    })

    result = calculate_symptom_percentages(sample_data)

    assert isinstance(result, pd.DataFrame)
    assert "Symptom" in result.columns
    assert "Percentage" in result.columns
    assert len(result) > 0

    print("test_calculate_symptom_percentages passed")


if __name__ == "__main__":
    test_load_pcos_data()
    test_calculate_symptom_percentages()
    print("All tests completed.")