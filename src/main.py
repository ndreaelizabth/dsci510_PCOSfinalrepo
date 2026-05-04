# AI generated: portions of this file were created with assistance of ChatGPT

import os

from config import RESULTS_DIR

from kaggle_pcosdata import (
    load_pcos_data,
    calculate_symptom_percentages,
    plot_symptom_prevalence
)

from reddit_api import (
    fetch_reddit_posts,
    count_reddit_symptoms,
    plot_reddit_symptoms
)

from PCOS_source_comparison import compare_symptoms

from medical_logisticregression import run_medical_logistic_regression
from medical_svm import run_medical_svm
from medical_randomforest import run_medical_random_forest
from medical_xgb import run_medical_xgboost
from lifestyle_analysis import run_lifestyle_analysis


def main():
    print("Starting PCOS project analysis...\n")

    # Set working directory to src/
    src_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(src_dir)

    # Make sure results folder exists inside src/
    os.makedirs(RESULTS_DIR, exist_ok=True)

    print(f"Working directory set to: {src_dir}")
    print(f"PNG files will be saved in: {os.path.join(src_dir, RESULTS_DIR)}")

    # Step 1: Medical symptom analysis
    print("\nRunning medical symptom analysis...")
    medical_df = load_pcos_data()
    medical_result = calculate_symptom_percentages(medical_df)
    print(medical_result)
    plot_symptom_prevalence(medical_result)

    # Step 2: Reddit symptom analysis
    print("\nRunning Reddit symptom analysis...")
    posts = fetch_reddit_posts()
    reddit_result = count_reddit_symptoms(posts)
    print(reddit_result)
    plot_reddit_symptoms(reddit_result)

    # Step 3: Compare medical vs Reddit
    print("\nRunning cross-source comparison...")
    comparison_df = compare_symptoms()
    print(comparison_df)

    # Step 4: Logistic Regression
    print("\nRunning Logistic Regression classifier...")
    logistic_result = run_medical_logistic_regression()
    print(logistic_result)

    # Step 5: Linear SVM
    print("\nRunning Linear SVM classifier...")
    svm_result = run_medical_svm()
    print(svm_result)

    # Step 6: Random Forest
    print("\nRunning Random Forest classifier and feature importance...")
    rf_result = run_medical_random_forest()
    print(rf_result)

    # Step 7: XGBoost
    print("\nRunning XGBoost classifier...")
    xgb_result = run_medical_xgboost()
    print(xgb_result)

    # Step 8: Lifestyle behavior analysis
    print("\nRunning lifestyle behavior analysis...")
    lifestyle_result = run_lifestyle_analysis()
    print(lifestyle_result)

    print("\nProject completed successfully.")
    print("Check PNG outputs in the src/results folder.")


if __name__ == "__main__":
    main()