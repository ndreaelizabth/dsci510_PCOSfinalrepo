#AI generated: portions of this file were created with assistance of ChatGPT

import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

from config import DATA_DIR, PCOS_DATA_FILE, RF_IMPORTANCE_CHART

PLOT_SIZE = (10, 6)
LINE_COLOR = "lavender"
DOT_COLOR = "purple"


def run_medical_random_forest(file_path=None):
    if file_path is None:
        file_path = os.path.join("..", DATA_DIR, PCOS_DATA_FILE)

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

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
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

    feature_importance["Symptom"] = feature_importance["Symptom"].str.replace("(Y/N)", "", regex=False)

    plt.figure(figsize=PLOT_SIZE)

    plt.hlines(
        y=feature_importance["Symptom"],
        xmin=0,
        xmax=feature_importance["Importance"],
        color=LINE_COLOR,
        linewidth=3
    )

    plt.plot(
        feature_importance["Importance"],
        feature_importance["Symptom"],
        "o",
        color=DOT_COLOR
    )

    plt.xlabel("Importance Score")
    plt.ylabel("Symptom")
    plt.title("Random Forest: Most Predictive Medical Symptoms")

    for i, value in enumerate(feature_importance["Importance"]):
        plt.text(value + 0.002, i, f"{value:.2f}", va='center')

    plt.tight_layout()
    plt.savefig(RF_IMPORTANCE_CHART)
    plt.show()

    return feature_importance


if __name__ == "__main__":
    run_medical_random_forest()