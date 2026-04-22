import pandas as pd
import matplotlib.pyplot as plt

from kaggle_pcosdata import load_pcos_data, calculate_symptom_percentages
from reddit_api import fetch_reddit_posts, count_reddit_symptoms


def prepare_medical_data():
    df = load_pcos_data()
    medical_df = calculate_symptom_percentages(df)

    medical_df = medical_df.copy()
    medical_df["Symptom"] = medical_df["Symptom"].str.replace("(Y/N)", "", regex=False)

    return medical_df


def prepare_reddit_data():
    posts = fetch_reddit_posts(total_limit=300)
    reddit_df = count_reddit_symptoms(posts)

    # rename Reddit labels so they match medical labels
    reddit_df = reddit_df.copy()
    reddit_df["Symptom"] = reddit_df["Symptom"].replace({
        "Cycle irregularity": "Cycle",
        "Weight gain": "Weight gain",
        "Hair growth": "hair growth",
        "Skin darkening": "Skin darkening ",
        "Hair loss": "Hair loss",
        "Pimples / acne": "Pimples",
        "Pimples": "Pimples"
    })

    return reddit_df


def compare_symptoms():
    medical_df = prepare_medical_data()
    reddit_df = prepare_reddit_data()

    # keep only the columns we need
    medical_df = medical_df.rename(columns={"Percentage": "Medical"})
    reddit_df = reddit_df.rename(columns={"Percentage_of_Posts": "Reddit"})

    merged = pd.merge(
        medical_df[["Symptom", "Medical"]],
        reddit_df[["Symptom", "Reddit"]],
        on="Symptom",
        how="inner"
    )

    print("\nMerged comparison table:")
    print(merged)

    merged.set_index("Symptom")[["Medical", "Reddit"]].plot(
        kind="bar",
        figsize=(10, 6),
        color=["lavender", "pink"]
    )

    plt.ylabel("Percentage")
    plt.title("Medical Study vs Reddit Symptom Comparison")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("comparison_chart.png")
    plt.show()

    return merged


if __name__ == "__main__":
    compare_symptoms()