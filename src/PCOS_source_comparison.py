# AI generated: portions of this file were created with assistance of ChatGPT

import pandas as pd
import matplotlib.pyplot as plt

from config import COMPARISON_CHART
from kaggle_pcosdata import load_pcos_data, calculate_symptom_percentages
from reddit_api import fetch_reddit_posts, count_reddit_symptoms

BAR_FIGSIZE = (11, 6)
BAR_COLORS = ["lavender", "#FFB6C1"]

KEEP_SYMPTOMS = [
    "Menstrual irregularity",
    "Weight gain",
    "Hair growth",
    "Skin darkening",
    "Hair loss",
    "Pimples"
]

SYMPTOM_NAME_STANDARDIZATION = {
    "Cycle(R/I)": "Menstrual irregularity",
    "Cycle length(days)": "Menstrual irregularity",
    "Cycle irregularity": "Menstrual irregularity",
    "Cycle length": "Menstrual irregularity",
    "Menstrual irregularity": "Menstrual irregularity",

    "Weight gain(Y/N)": "Weight gain",
    "Weight gain": "Weight gain",

    "hair growth(Y/N)": "Hair growth",
    "Hair growth": "Hair growth",

    "Skin darkening (Y/N)": "Skin darkening",
    "Skin darkening": "Skin darkening",

    "Hair loss(Y/N)": "Hair loss",
    "Hair loss": "Hair loss",

    "Pimples(Y/N)": "Pimples",
    "Pimples": "Pimples",
    "Pimples / acne": "Pimples",
    "Pimples/acne": "Pimples",
    "Acne": "Pimples",
}


def standardize_symptom_names(df):
    df = df.copy()
    df["Symptom"] = df["Symptom"].replace(SYMPTOM_NAME_STANDARDIZATION)
    return df


def prepare_medical_data():
    df = load_pcos_data()
    medical_df = calculate_symptom_percentages(df).copy()

    medical_df = standardize_symptom_names(medical_df)
    medical_df = medical_df[medical_df["Symptom"].isin(KEEP_SYMPTOMS)]

    # In case multiple columns map to the same category
    medical_df = medical_df.groupby("Symptom", as_index=False)["Percentage"].mean()

    # Use "Medical Dataset" consistently everywhere
    medical_df = medical_df.rename(columns={"Percentage": "Medical Dataset"})

    return medical_df[["Symptom", "Medical Dataset"]]


def prepare_reddit_data():
    posts = fetch_reddit_posts()
    reddit_df = count_reddit_symptoms(posts).copy()

    reddit_df = standardize_symptom_names(reddit_df)
    reddit_df = reddit_df[reddit_df["Symptom"].isin(KEEP_SYMPTOMS)]

    if "Percentage_of_Posts" in reddit_df.columns:
        reddit_df["Reddit Posts"] = reddit_df["Percentage_of_Posts"]
    elif "Percentage_of_Threads" in reddit_df.columns:
        reddit_df["Reddit Posts"] = reddit_df["Percentage_of_Threads"]
    else:
        reddit_df["Reddit Posts"] = (reddit_df["Count"] / len(posts)) * 100

    reddit_df = reddit_df.groupby("Symptom", as_index=False)["Reddit Posts"].mean()

    return reddit_df[["Symptom", "Reddit Posts"]]


def compare_symptoms():
    medical_df = prepare_medical_data()
    reddit_df = prepare_reddit_data()

    print("\nMedical symptoms found:")
    print(medical_df)

    print("\nReddit symptoms found:")
    print(reddit_df)

    merged = pd.merge(
        medical_df,
        reddit_df,
        on="Symptom",
        how="inner"
    )

    merged = merged.sort_values(by="Medical Dataset", ascending=False)

    print("\nComparison table:")
    print(merged)

    print("\nMerged columns:")
    print(merged.columns)

    ax = merged.set_index("Symptom")[["Medical Dataset", "Reddit Posts"]].plot(
        kind="bar",
        figsize=BAR_FIGSIZE,
        color=BAR_COLORS
    )

    plt.title("Medical Dataset vs Reddit: Observable PCOS Symptom Comparison")
    plt.xlabel("Observable PCOS symptom category")
    plt.ylabel("Percentage of medical cases or Reddit posts with symptom (%)")
    plt.xticks(rotation=35, ha="right")
    plt.legend(title="Data Source")

    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f", padding=3, fontsize=9)

    plt.tight_layout()
    plt.savefig(COMPARISON_CHART)
    plt.show()

    merged["Difference"] = merged["Reddit Posts"] - merged["Medical Dataset"]

    print("\nDifference table (Reddit Posts - Medical Dataset):")
    print(merged[["Symptom", "Difference"]])

    return merged


if __name__ == "__main__":
    compare_symptoms()