# AI generated: portions of this file were created with assistance of ChatGPT

import os

from config import RESULTS_DIR

from kaggle_pcosdata import load_pcos_data, calculate_symptom_percentages, plot_symptom_prevalence
from reddit_api import fetch_reddit_posts, count_reddit_symptoms, plot_reddit_symptoms
from PCOS_source_comparison import compare_symptoms
from medical_logisticregression import run_medical_logistic_regression
from medical_svm import run_medical_svm
from medical_randomforest import run_medical_random_forest
from medical_xgb import run_medical_xgboost
from lifestyle_analysis import run_lifestyle_analysis


if __name__ == "__main__":
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # --- Medical Dataset ---
    # Load Kaggle PCOS data and analyze observable symptoms
    medical_df = load_pcos_data()
    medical_result = calculate_symptom_percentages(medical_df)

    print("\nMedical Symptom Results:")
    print(medical_result)

    plot_symptom_prevalence(medical_result)
    print("\n" + "=" * 50 + "\n")

    # --- Reddit Data ---
    # Fetch Reddit posts and analyze patient-reported symptoms
    posts = fetch_reddit_posts()
    reddit_result = count_reddit_symptoms(posts)

    print("\nReddit Symptom Results:")
    print(reddit_result)

    plot_reddit_symptoms(reddit_result)
    print("\n" + "=" * 50 + "\n")

    # --- Medical vs Reddit Comparison ---
    comparison_df = compare_symptoms()

    print("\nMedical vs Reddit Comparison:")
    print(comparison_df)
    print("\n" + "=" * 50 + "\n")

    # --- Machine Learning Models ---
    logistic_result = run_medical_logistic_regression()
    print("\nLogistic Regression Results:")
    print(logistic_result)
    print("\n" + "=" * 50 + "\n")

    svm_result = run_medical_svm()
    print("\nSVM Results:")
    print(svm_result)
    print("\n" + "=" * 50 + "\n")

    rf_result = run_medical_random_forest()
    print("\nRandom Forest Results:")
    print(rf_result)
    print("\n" + "=" * 50 + "\n")

    xgb_result = run_medical_xgboost()
    print("\nXGBoost Results:")
    print(xgb_result)
    print("\n" + "=" * 50 + "\n")

    # --- Lifestyle Data ---
    lifestyle_result = run_lifestyle_analysis()

    print("\nLifestyle Behavior Results:")
    print(lifestyle_result)
    print("\n" + "=" * 50 + "\n")