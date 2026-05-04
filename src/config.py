#AI generated: portions of this file were created with assistance of ChatGPT

from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Project directories
DATA_DIR = "data"
RESULTS_DIR = "results"

# Data files
PCOS_DATA_FILE = "PCOS_data.csv"
LIFESTYLE_DATA_FILE = "diet_exercise_PCOSinsights.csv"

# Reddit configuration
REDDIT_SUBREDDIT = "PCOS"
REDDIT_TOTAL_LIMIT = 300
REDDIT_BATCH_SIZE = 100
REDDIT_USER_AGENT = "dsci510_PCOSfinal/1.0"

# Output files saved inside src/results/
MEDICAL_SYMPTOM_CHART = f"{RESULTS_DIR}/pcos_symptom_prevalence.png"
REDDIT_SYMPTOM_CHART = f"{RESULTS_DIR}/reddit_symptom_prevalence.png"
COMPARISON_CHART = f"{RESULTS_DIR}/comparison_chart.png"
RF_IMPORTANCE_CHART = f"{RESULTS_DIR}/medical_random_forest_lollipop.png"
LIFESTYLE_BEHAVIOR_CHART = f"{RESULTS_DIR}/lifestyle_behavior_factors.png"

LOGISTIC_REGRESSION_CHART = f"{RESULTS_DIR}/medical_logistic_regression.png"
SVM_CHART = f"{RESULTS_DIR}/medical_svm.png"
XGBOOST_CHART = f"{RESULTS_DIR}/medical_xgboost.png"

# Symptom labels used across analyses
SYMPTOM_COLUMNS = [
    "Cycle(R/I)",
    "Cycle length(days)",
    "Weight gain(Y/N)",
    "hair growth(Y/N)",
    "Skin darkening (Y/N)",
    "Hair loss(Y/N)",
    "Pimples(Y/N)",
]

# Clean display names
SYMPTOM_NAME_MAP = {
    "Cycle(R/I)": "Cycle irregularity",
    "Cycle length(days)": "Cycle length",
    "Weight gain(Y/N)": "Weight gain",
    "hair growth(Y/N)": "Hair growth",
    "Skin darkening (Y/N)": "Skin darkening",
    "Hair loss(Y/N)": "Hair loss",
    "Pimples(Y/N)": "Pimples",
}