# AI generated: portions of this file were created with assistance of ChatGPT

import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt

from config import DATA_DIR, PCOS_DATA_FILE

PLOT_SIZE = (10, 6)
LINE_COLOR = "lavender"
DOT_COLOR = "purple"


def run_medical_logistic_regression(file_path=None):
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

    # Convert cycle regularity to numeric
    if X["Cycle(R/I)"].dtype == object:
        X["Cycle(R/I)"] = X["Cycle(R/I)"].map({"R": 0, "I": 1})

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    lr = LogisticRegression(max_iter=1000)
    lr.fit(X_train, y_train)

    y_pred = lr.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    error = 1 - accuracy
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    print("\nLogistic Regression Model Performance:")
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Error: {error:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1-score: {f1:.2f}")

    rename_map = {
        "Cycle(R/I)": "Cycle irregularity",
        "Cycle length(days)": "Cycle length",
        "Weight gain(Y/N)": "Weight gain",
        "hair growth(Y/N)": "Hair growth",
        "Skin darkening (Y/N)": "Skin darkening",
        "Hair loss(Y/N)": "Hair loss",
        "Pimples(Y/N)": "Pimples"
    }

    coefficients = pd.DataFrame({
        "Symptom": X.columns,
        "Coefficient": lr.coef_[0]
    })

    coefficients["Symptom"] = coefficients["Symptom"].map(rename_map)
    coefficients = coefficients.sort_values(by="Coefficient", ascending=True)

    print("\nLogistic Regression Coefficients:")
    print(coefficients)

    plt.figure(figsize=PLOT_SIZE)

    plt.hlines(
        y=coefficients["Symptom"],
        xmin=0,
        xmax=coefficients["Coefficient"],
        color=LINE_COLOR,
        linewidth=3
    )

    plt.plot(
        coefficients["Coefficient"],
        coefficients["Symptom"],
        "o",
        color=DOT_COLOR
    )

    plt.axvline(x=0, color="gray", linestyle="--", linewidth=1)

    plt.xlabel("Coefficient value: effect on predicted PCOS likelihood")
    plt.ylabel("Observable symptom(s)")
    plt.title("Logistic Regression: Observable Symptoms Predicting PCOS")

    for i, value in enumerate(coefficients["Coefficient"]):
        offset = 0.02 if value >= 0 else -0.15
        plt.text(value + offset, i, f"{value:.2f}", va="center")

    metrics_text = (
        f"Logistic Regression Performance\n"
        f"Accuracy: {accuracy:.2f}\n"
        f"Error: {error:.2f}\n"
        f"Precision: {precision:.2f}\n"
        f"Recall: {recall:.2f}\n"
        f"F1-score: {f1:.2f}"
    )

    plt.text(
        0.68,
        0.15,
        metrics_text,
        transform=plt.gca().transAxes,
        fontsize=10,
        ha="left",
        bbox=dict(
            facecolor="lavender",
            boxstyle="round",
            pad=0.5
        )
    )

    plt.tight_layout()
    plt.show()

    return coefficients


if __name__ == "__main__":
    run_medical_logistic_regression()
