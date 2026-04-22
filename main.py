import os

from src.kaggle_pcosdata import load_pcos_data, calculate_symptom_percentages, plot_symptom_prevalence
from src.reddit_api import fetch_reddit_posts, count_reddit_symptoms, plot_reddit_symptoms
from src.PCOS_source_comparison import compare_symptoms
from src.medical_random_forest import run_medical_random_forest


def main():
    print("Starting PCOS project analysis...\n")

    # Make sure results folder exists
    os.makedirs("results", exist_ok=True)

    # Step 1: Medical symptom analysis
    print("Running medical symptom analysis...")
    medical_df = load_pcos_data()
    medical_result = calculate_symptom_percentages(medical_df)
    print(medical_result)
    plot_symptom_prevalence(medical_result)

    # Step 2: Reddit symptom analysis
    print("\nRunning Reddit symptom analysis...")
    posts = fetch_reddit_posts(total_limit=300)
    reddit_result = count_reddit_symptoms(posts)
    print(reddit_result)
    plot_reddit_symptoms(reddit_result)

    # Step 3: Compare medical vs Reddit
    print("\nRunning cross-source comparison...")
    comparison_df = compare_symptoms()
    print(comparison_df)

    # Step 4: Random Forest medical feature importance
    print("\nRunning Random Forest feature importance...")
    rf_result = run_medical_random_forest()
    print(rf_result)

    print("\nProject completed successfully.")
    print("Check generated charts and outputs in your project files/results folder.")


if __name__ == "__main__":
    main()