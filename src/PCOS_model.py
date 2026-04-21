import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from kaggle_pcosdata import load_pcos_data


def run_pcos_models():
    df = load_pcos_data()

    # Drop junk column if it exists
    if "Unnamed: 44" in df.columns:
        df = df.drop(columns=["Unnamed: 44"])

    # Drop ID columns that should not be used for prediction
    drop_cols = ["Sl. No", "Patient File No."]
    for col in drop_cols:
        if col in df.columns:
            df = df.drop(columns=[col])

    # Fill only small missing values instead of dropping almost all rows
    df = df.fillna(df.median(numeric_only=True))

    print("Dataset shape after cleaning:")
    print(df.shape)

    target_col = "PCOS (Y/N)"
    print(f"Target column: {target_col}")

    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Keep only numeric columns
    X = X.select_dtypes(include=["number"])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Logistic Regression
    lr = LogisticRegression(max_iter=2000)
    lr.fit(X_train, y_train)
    lr_preds = lr.predict(X_test)

    print("\nLogistic Regression Accuracy:")
    print(accuracy_score(y_test, lr_preds))
    print("\nLogistic Regression Report:")
    print(classification_report(y_test, lr_preds))

    # Random Forest
    rf = RandomForestClassifier(random_state=42)
    rf.fit(X_train, y_train)
    rf_preds = rf.predict(X_test)

    print("\nRandom Forest Accuracy:")
    print(accuracy_score(y_test, rf_preds))
    print("\nRandom Forest Report:")
    print(classification_report(y_test, rf_preds))

    # Feature importance
    feature_importance = pd.Series(rf.feature_importances_, index=X.columns)
    feature_importance = feature_importance.sort_values(ascending=False)

    print("\nTop 10 Random Forest Features:")

    symptom_cols = [
    "Weight gain(Y/N)",
    "hair growth(Y/N)",
    "Skin darkening (Y/N)",
    "Hair loss(Y/N)",
    "Pimples(Y/N)",
    "Cycle length(days)",
    "Cycle(R/I)"
]
    symptom_importance = feature_importance[feature_importance.index.isin(symptom_cols)]

    print(symptom_importance.sort_values(ascending=False))


if __name__ == "__main__":
    df = load_pcos_data()
    print("Dataset loaded successfully.")
    print("Shape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nFirst 10 rows:")
    print(df.head(10))
    print("\nMissing values per column:")
    print(df.isna().sum())