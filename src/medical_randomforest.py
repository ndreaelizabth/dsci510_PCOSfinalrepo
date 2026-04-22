#AI generated: portions of this file were created with assistance of ChatGPT

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

from kaggle_pcosdata import load_pcos_data

def run_medical_random_forest(file_path="../data/PCOS_data.csv"):
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
        "Fast food (Y/N)"
    ]

    df = df[cols].copy()

    X = df.drop(columns=["PCOS (Y/N)"])
    y = df["PCOS (Y/N)"]

    # Convert Cycle(R/I) if needed
    if X["Cycle(R/I)"].dtype == object:
        X["Cycle(R/I)"] = X["Cycle(R/I)"].map({"R": 0, "I": 1})

    rf = RandomForestClassifier(random_state=42)
    rf.fit(X, y)


    feature_importance = pd.DataFrame({
        "Symptom": X.columns,
        "Importance": rf.feature_importances_
    })

    feature_importance = feature_importance.sort_values(by="Importance", ascending=True)

    print("\nRandom Forest Feature Importance:")
    print(feature_importance)

    # Clean labels
    feature_importance["Symptom"] = feature_importance["Symptom"].str.replace("(Y/N)", "", regex=False)

    plt.figure(figsize=(10, 6))

    # Draw horizontal lines
    plt.hlines(
        y=feature_importance["Symptom"],
        xmin=0,
        xmax=feature_importance["Importance"],
        color="lavender",
        linewidth=3
    )

    # Draw dots
    plt.plot(
        feature_importance["Importance"],
        feature_importance["Symptom"],
        "o",
        color="purple"
    )

    # Labels
    plt.xlabel("Importance Score")
    plt.ylabel("Symptom")
    plt.title("Random Forest: Most Predictive Medical Symptoms")

    # Add values next to dots
    for i, value in enumerate(feature_importance["Importance"]):
        plt.text(value + 0.002, i, f"{value:.2f}", va='center')

    plt.tight_layout()
    plt.savefig("medical_random_forest_lollipop.png")
    plt.show()

    return feature_importance


if __name__ == "__main__":
    run_medical_random_forest()