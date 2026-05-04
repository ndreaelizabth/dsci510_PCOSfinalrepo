#AI generated: portions of this file were created with assistance of ChatGPT

from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
env_path = Path(__file__).resolve().parent / ".env"
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

# Output files
MEDICAL_SYMPTOM_CHART = "pcos_symptom_prevalence.png"
REDDIT_SYMPTOM_CHART = "reddit_symptom_prevalence.png"
COMPARISON_CHART = "comparison_chart.png"
SCATTERPLOT_CHART = "symptom_scatterplot.png"
RF_IMPORTANCE_CHART = "medical_random_forest_lollipop.png"

# Symptom labels used across analyses
SYMPTOM_COLUMNS = [
    "Cycle(R/I)",
    "Cycle length(days)",
    "Weight gain(Y/N)",
    "hair growth(Y/N)",
    "Skin darkening (Y/N)",
    "Hair loss(Y/N)",
    "Pimples(Y/N)",
    "Fast food (Y/N)",
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
    "Fast food (Y/N)": "Fast food",
}