#AI generated: portions of this file were created with assistance of ChatGPT

import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
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
        "Pimples(Y/N)"
    ]

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    df = df[cols].copy()
    df = df.dropna()

    X = df.drop(columns=["PCOS (Y/N)"])
    y = df["PCOS (Y/N)"]

    if X["Cycle(R/I)"].dtype == object:
        X["Cycle(R/I)"] = X["Cycle(R/I)"].map({"R": 0, "I": 1})

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    rf = RandomForestClassifier(random_state=42)
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    print("\nRandom Forest Model Performance:")
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1-score: {f1:.2f}")

    feature_importance = pd.DataFrame({
        "Symptom": X.columns,
        "Importance": rf.feature_importances_
    })

    rename_map = {  
    "Cycle(R/I)": "Cycle irregularity",
    "Cycle length(days)": "Cycle length",
    "Weight gain(Y/N)": "Weight gain",
    "hair growth(Y/N)": "Hair growth",
    "Skin darkening (Y/N)": "Skin darkening",
    "Hair loss(Y/N)": "Hair loss",
    "Pimples(Y/N)": "Pimples"
}

    feature_importance["Symptom"] = feature_importance["Symptom"].map(rename_map)
    feature_importance = feature_importance.sort_values(by="Importance", ascending=True)

    print("\nRandom Forest Feature Importance:")
    print(feature_importance)

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

    plt.xlabel("Feature importance score for predicting PCOS")
    plt.ylabel("Observable symptom(s)")
    plt.title("Random Forest: Observable Symptoms Predicting PCOS")

    for i, value in enumerate(feature_importance["Importance"]):
        plt.text(value + 0.002, i, f"{value:.2f}", va="center")
    
    metrics_text = (
        f"Random Forest Performance\n"
        f"Accuracy: {accuracy:.2f}\n"
        f"Precision: {precision:.2f}\n"
        f"Recall: {recall:.2f}\n"
        f"F1-score: {f1:.2f}"
)

    plt.text(
        0.72, 0.15,  
        metrics_text,
        transform=plt.gca().transAxes,
        fontsize=10,
        ha="left",  # align text nicely inside box
        bbox=dict(
            facecolor="lavender",     # lavender background
            boxstyle="round", pad=0.5, 
        )
    )

    plt.tight_layout()
    plt.savefig(RF_IMPORTANCE_CHART)
    plt.show()

    return feature_importance


if __name__ == "__main__":
    run_medical_random_forest()