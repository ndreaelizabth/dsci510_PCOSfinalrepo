import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from src.kaggle_pcosdata import load_pcos_data


def run_pcos_models():
    df = load_pcos_data()

    # remove missing values for a simple first version
    df = df.dropna()

    print("Dataset shape after dropping missing values:")
    print(df.shape)

    # use last column as target for now
    target_col = df.columns[-1]
    print(f"Target column: {target_col}")

    X = df.drop(columns=[target_col])
    y = df[target_col]

    # keep only numeric columns
    X = X.select_dtypes(include=["number"])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Logistic Regression
    lr = LogisticRegression(max_iter=1000)
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
    print(feature_importance.head(10))


if __name__ == "__main__":
    run_pcos_models()