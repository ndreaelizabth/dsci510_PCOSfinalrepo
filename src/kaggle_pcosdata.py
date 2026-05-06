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
    ]

    df = df[cols].copy()
    df = df.dropna()

    # Keep only patients diagnosed with PCOS
    df = df[df["PCOS (Y/N)"] == 1]

    print("Filtered dataset shape (only PCOS patients):")
    print(df.shape)

    return df


def is_yes(series):
    """
    Handles columns that may be stored as 1/0, Y/N, Yes/No, or strings.
    """
    return series.astype(str).str.strip().str.lower().isin(
        ["1", "y", "yes", "true"]
    )


def is_menstrual_irregularity(df):
    """
    Combines Cycle(R/I) and Cycle length(days) into one category
    to match the Reddit category: Menstrual irregularity.
    """

    cycle_status = df["Cycle(R/I)"]

    # Handles object values like R/I, Regular/Irregular
    if cycle_status.dtype == object:
        irregular_from_status = cycle_status.astype(str).str.strip().str.lower().isin(
            ["i", "irregular"]
        )
    else:
        # Handles common numeric encodings:
        # 1 can mean irregular in some cleaned datasets.
        # 4 can mean irregular in the original PCOS dataset.
        irregular_from_status = cycle_status.isin([1, 4])

    cycle_length = pd.to_numeric(df["Cycle length(days)"], errors="coerce")

    # Common menstrual cycle range used for flagging irregular length
    irregular_from_length = (cycle_length < 21) | (cycle_length > 35)

    return irregular_from_status | irregular_from_length


def calculate_symptom_percentages(df):
    results = {
        "Menstrual irregularity": is_menstrual_irregularity(df).mean() * 100,
        "Weight gain": is_yes(df["Weight gain(Y/N)"]).mean() * 100,
        "Hair growth": is_yes(df["hair growth(Y/N)"]).mean() * 100,
        "Skin darkening": is_yes(df["Skin darkening (Y/N)"]).mean() * 100,
        "Hair loss": is_yes(df["Hair loss(Y/N)"]).mean() * 100,
        "Pimples": is_yes(df["Pimples(Y/N)"]).mean() * 100,
    }

    result_df = pd.DataFrame(
        list(results.items()),
        columns=["Symptom", "Percentage"]
    )

    result_df = result_df.sort_values(
        by="Percentage",
        ascending=False
    )

    return result_df


def plot_symptom_prevalence(result_df):
    plt.figure(figsize=PLOT_SIZE)

    plt.barh(
        result_df["Symptom"],
        result_df["Percentage"],
        color=BAR_COLOR
    )

    plt.xlabel("Percentage of diagnosed PCOS patients with symptom (%)")
    plt.ylabel("Medical observable symptom category")
    plt.title("Medical Dataset: Observable Symptoms Among Diagnosed PCOS Patients")

    for i, value in enumerate(result_df["Percentage"]):
        plt.text(value + 0.5, i, f"{value:.1f}%", va="center")

    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(MEDICAL_SYMPTOM_CHART)
    plt.close()


if __name__ == "__main__":
    df = load_pcos_data()

    print("Dataset loaded successfully.")
    print(f"Shape: {df.shape}")
    print(df.head())

    result = calculate_symptom_percentages(df)

    print("\nMedical observable symptom prevalence among diagnosed PCOS patients:")
    print(result)

    plot_symptom_prevalence(result)