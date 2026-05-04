# AI generated: portions of this file were created with assistance of ChatGPT

import os
import pandas as pd
import matplotlib.pyplot as plt

from config import LIFESTYLE_DATA_FILE, DATA_DIR, LIFESTYLE_BEHAVIOR_CHART

PLOT_SIZE = (11, 6)
BAR_COLORS = ["lavender", "#FFB6C1"]
LIFESTYLE_CHART = "lifestyle_behavior_factors.png"


def load_lifestyle_data(file_path=None):
    if file_path is None:
        file_path = os.path.join("..", DATA_DIR, LIFESTYLE_DATA_FILE)

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    return df


def clean_pcos_column(df):
    df = df.copy()

    df["PCOS"] = df["PCOS"].astype(str).str.strip().str.lower()

    df["PCOS_Status"] = df["PCOS"].map({
        "1": "PCOS",
        "0": "No PCOS",
        "yes": "PCOS",
        "no": "No PCOS",
        "y": "PCOS",
        "n": "No PCOS",
        "true": "PCOS",
        "false": "No PCOS"
    })

    df = df.dropna(subset=["PCOS_Status"])

    return df


def encode_lifestyle_column(series):
    """
    Converts lifestyle values into numbers.
    Numeric columns stay numeric.
    Text categories like low/moderate/high are converted into ordered scores.
    """

    numeric_series = pd.to_numeric(series, errors="coerce")

    if numeric_series.notna().sum() > 0:
        return numeric_series

    cleaned = series.astype(str).str.strip().str.lower()

    mapping = {
        "never": 0,
        "none": 0,
        "no": 0,
        "n": 0,
        "false": 0,

        "rarely": 1,
        "low": 1,

        "sometimes": 2,
        "moderate": 2,
        "medium": 2,

        "often": 3,
        "regularly": 3,
        "high": 3,

        "daily": 4,
        "very high": 4,

        "yes": 1,
        "y": 1,
        "true": 1
    }

    return cleaned.map(mapping)


def prepare_lifestyle_behavior_data(df):
    lifestyle_columns = [
        "Stress_Level",
        "Sleep_Hours",
        "Exercise_Frequency",
        "Diet_Sweets",
        "Diet_Fried_Food"
    ]

    available_columns = [col for col in lifestyle_columns if col in df.columns]

    if not available_columns:
        raise ValueError("None of the selected lifestyle behavior columns were found.")

    encoded_df = df[["PCOS_Status"]].copy()

    for col in available_columns:
        encoded_df[col] = encode_lifestyle_column(df[col])

    encoded_df = encoded_df.dropna(axis=1, how="all")

    return encoded_df


def normalize_lifestyle_scores(encoded_df):
    """
    Normalizes each lifestyle factor from 0 to 1 so they can be compared
    on the same chart even if the original columns used different scales.
    """

    normalized_df = encoded_df.copy()

    for col in normalized_df.columns:
        if col == "PCOS_Status":
            continue

        min_value = normalized_df[col].min()
        max_value = normalized_df[col].max()

        if max_value != min_value:
            normalized_df[col] = (
                (normalized_df[col] - min_value) / (max_value - min_value)
            )
        else:
            normalized_df[col] = 0

    return normalized_df


def calculate_group_averages(normalized_df):
    averages = normalized_df.groupby("PCOS_Status").mean(numeric_only=True)

    averages = averages.T.reset_index()
    averages = averages.rename(columns={"index": "Lifestyle Factor"})

    return averages


def clean_lifestyle_labels(averages):
    averages = averages.copy()

    label_map = {
        "Stress_Level": "Stress level",
        "Sleep_Hours": "Sleep hours",
        "Exercise_Frequency": "Exercise frequency",
        "Diet_Sweets": "Sweets intake",
        "Diet_Fried_Food": "Fried food intake"
    }

    averages["Lifestyle Factor"] = averages["Lifestyle Factor"].replace(label_map)

    return averages


def plot_lifestyle_behavior_factors(averages):
    averages = clean_lifestyle_labels(averages)

    ax = averages.set_index("Lifestyle Factor").plot(
        kind="bar",
        figsize=PLOT_SIZE,
        color=BAR_COLORS
    )

    plt.title("Lifestyle Behavior Factors by PCOS Diagnosis")
    plt.xlabel("Lifestyle behavior factor")
    plt.ylabel("Average normalized lifestyle score")
    plt.xticks(rotation=35, ha="right")
    plt.legend(title="Diagnosis Status")

    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f", padding=3, fontsize=8)

    plt.tight_layout()
    plt.savefig(LIFESTYLE_BEHAVIOR_CHART)
    plt.close()


def run_lifestyle_analysis():
    df = load_lifestyle_data()
    df = clean_pcos_column(df)

    encoded_df = prepare_lifestyle_behavior_data(df)

    print("\nRaw encoded lifestyle values preview:")
    print(encoded_df.head())

    normalized_df = normalize_lifestyle_scores(encoded_df)

    averages = calculate_group_averages(normalized_df)

    print("\nAverage normalized lifestyle scores by PCOS diagnosis:")
    print(clean_lifestyle_labels(averages))

    plot_lifestyle_behavior_factors(averages)

    return averages


if __name__ == "__main__":
    run_lifestyle_analysis()