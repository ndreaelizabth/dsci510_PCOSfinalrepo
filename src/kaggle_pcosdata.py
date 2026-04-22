#AI generated: portions of this file were created with assistance of ChatGPT

import os
import pandas as pd
import matplotlib.pyplot as plt

from config import DATA_DIR, PCOS_DATA_FILE, MEDICAL_SYMPTOM_CHART

PLOT_SIZE = (10, 6)
BAR_COLOR = "lavender"


def load_pcos_data(file_path=None):
    if file_path is None:
        file_path = os.path.join("..", DATA_DIR, PCOS_DATA_FILE)

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    cols = [
        "PCOS (Y/N)",
        "Cycle(R/I)",
        "Cycle length(days)",
        "Weight gain(Y/N)",
        "hair growth(Y/N)",
        "Skin darkening (Y/N)",
        "Hair loss(Y/N)",
        "Pimples(Y/N)",
        "Fast food (Y/N)",
    ]

    df = df[cols]
    df = df[df["PCOS (Y/N)"] == 1]

    print("Filtered dataset shape (only PCOS patients):")
    print(df.shape)

    return df


def calculate_symptom_percentages(df):
    symptom_cols = [
        "Weight gain(Y/N)",
        "hair growth(Y/N)",
        "Skin darkening (Y/N)",
        "Hair loss(Y/N)",
        "Pimples(Y/N)",
        "Fast food (Y/N)",
    ]

    results = {}

    for col in symptom_cols:
        percent = (df[col] == 1).mean() * 100
        results[col] = percent

    result_df = pd.DataFrame(list(results.items()), columns=["Symptom", "Percentage"])
    result_df = result_df.sort_values(by="Percentage", ascending=False)

    return result_df


def plot_symptom_prevalence(result_df):
    result_df = result_df.copy()
    result_df["Symptom"] = result_df["Symptom"].str.replace("(Y/N)", "", regex=False)

    plt.figure(figsize=PLOT_SIZE)
    plt.barh(result_df["Symptom"], result_df["Percentage"], color=BAR_COLOR)
    plt.xlabel("Percentage of PCOS Patients (%)")
    plt.ylabel("Symptom")
    plt.title("Most Common Symptoms Among PCOS Patients")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(MEDICAL_SYMPTOM_CHART)
    plt.show()


if __name__ == "__main__":
    df = load_pcos_data()
    print("Dataset loaded successfully.")
    print(f"Shape: {df.shape}")
    print(df.head())

    result = calculate_symptom_percentages(df)
    print("\nSymptom prevalence among PCOS patients:")
    print(result)

    plot_symptom_prevalence(result)