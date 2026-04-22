#AI generated: portions of this file were created with assistance of ChatGPT

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

from kaggle_pcosdata import load_pcos_data, calculate_symptom_percentages
from reddit_api import fetch_reddit_posts, count_reddit_symptoms

def prepare_medical_data():
    df = load_pcos_data()
    medical_df = calculate_symptom_percentages(df).copy()

    medical_df["Symptom"] = medical_df["Symptom"].replace({
        "Weight gain(Y/N)": "Weight gain",
        "hair growth(Y/N)": "Hair growth",
        "Skin darkening (Y/N)": "Skin darkening",
        "Hair loss(Y/N)": "Hair loss",
        "Pimples(Y/N)": "Pimples",
        "Fast food (Y/N)": "Fast food"
    })

    medical_df = medical_df.rename(columns={"Percentage": "Medical"})
    return medical_df[["Symptom", "Medical"]]


def prepare_reddit_data():
    posts = fetch_reddit_posts(total_limit=300)
    reddit_df = count_reddit_symptoms(posts).copy()

    reddit_df["Symptom"] = reddit_df["Symptom"].replace({
        "Weight gain": "Weight gain",
        "Hair growth": "Hair growth",
        "Skin darkening": "Skin darkening",
        "Hair loss": "Hair loss",
        "Pimples / acne": "Pimples",
        "Pimples": "Pimples",
        "Fast food": "Fast food"
    })

    # keep only symptoms you want to compare directly
    keep_symptoms = [
        "Weight gain",
        "Hair growth",
        "Skin darkening",
        "Hair loss",
        "Pimples",
        "Fast food"
    ]
    reddit_df = reddit_df[reddit_df["Symptom"].isin(keep_symptoms)]

    # convert Reddit counts into percentage of total symptom mentions
    total_mentions = reddit_df["Count"].sum()
    reddit_df["Reddit"] = (reddit_df["Count"] / total_mentions) * 100

    return reddit_df[["Symptom", "Reddit"]]


def compare_symptoms():
    medical_df = prepare_medical_data()
    reddit_df = prepare_reddit_data()

    merged = pd.merge(medical_df, reddit_df, on="Symptom", how="inner")

    merged = merged.sort_values(by="Medical", ascending=False)

    print("\nComparison table:")
    print(merged)

    ax = merged.set_index("Symptom")[["Medical", "Reddit"]].plot(
        kind="bar",
        figsize=(11, 6),
        color=["lavender", "#FFB6C1"]
    )

    plt.title("Medical Study vs Reddit Symptom Comparison")
    plt.xlabel("Symptom")
    plt.ylabel("Percentage (%)")
    plt.xticks(rotation=35, ha="right")
    plt.legend(title="Source")

    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f", padding=3, fontsize=9)

    plt.tight_layout()
    plt.savefig("comparison_chart.png")
    plt.show()

    merged["Difference"] = merged["Reddit"] - merged["Medical"]

    print("\nDifference table (Reddit - Medical):")
    print(merged[["Symptom", "Difference"]])

    plot_scatter_comparison(merged)
    calculate_spearman_correlation(merged)

    return merged

def plot_scatter_comparison(merged):
    plt.figure(figsize=(8, 6))
    plt.scatter(merged["Medical"], merged["Reddit"], color="purple")

    for _, row in merged.iterrows():
        plt.annotate(
            row["Symptom"],
            (row["Medical"], row["Reddit"]),
            textcoords="offset points",
            xytext=(5, 5)
        )

    plt.xlabel("Medical Symptom Percentage")
    plt.ylabel("Reddit Symptom Percentage")
    plt.title("Scatterplot: Medical vs Reddit Symptoms")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("symptom_scatterplot.png")
    plt.show()


def calculate_spearman_correlation(merged):
    corr, p_value = spearmanr(merged["Medical"], merged["Reddit"])

    print("\nSpearman Correlation Results:")
    print(f"Correlation coefficient: {corr:.3f}")
    print(f"P-value: {p_value:.3f}")

    return corr, p_value


if __name__ == "__main__":
    compare_symptoms()