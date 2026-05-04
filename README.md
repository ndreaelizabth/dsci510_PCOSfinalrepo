DSCI 510 – Spring 2026 – University of Southern California
Instructor: Dr. Alexey Tregubov

# PCOS Symptoms: Medical Records vs. Patient Voices

## Introduction

This project explores how PCOS symptoms appear across medical records, Reddit patient discussions, and lifestyle data. Using a medical PCOS dataset, r/PCOS Reddit posts, and a lifestyle dataset, the project compares medically recorded observable symptoms with symptoms patients discuss online.

The analysis focuses on observable symptoms such as menstrual irregularity, weight gain, hair growth, skin darkening, hair loss, and pimples. It also uses machine learning classifiers to test whether these symptoms can help predict PCOS diagnosis in the medical dataset. Finally, lifestyle factors such as stress, sleep, exercise frequency, sweets intake, and fried food intake are analyzed to provide additional context for PCOS management.

## Data sources

1. Kaggle PCOS Medical dataset (CSV): https://www.kaggle.com/datasets/shreyasvedpathak/pcos-dataset
2. Reddit API - r/PCOS subreddit: https://www.reddit.com/r/PCOS/
3. Kaggle PCOS Lifestlye dataset (CSV): https://www.kaggle.com/datasets/hasaanrana/diet-exercise-and-pcos-insights?resource=download
 
| Source | Description | Data Used |
|---|---|---|
| Kaggle PCOS Medical Dataset | Provides structured medical data for patients with and without PCOS. | PCOS diagnosis, menstrual cycle irregularity, cycle length, weight gain, hair growth, skin darkening, hair loss, pimples |
| Reddit API - r/PCOS | Provides patient-written posts that reflect real-life PCOS experiences and symptom discussions. | Post title, post body text, Reddit score, number of comments, date posted, post permalink |
| Kaggle PCOS Lifestyle Dataset | Provides lifestyle behavior data related to PCOS diagnosis and management. | PCOS diagnosis, stress level, exercise frequency, sweets intake, fried food intake |

## Analysis 

This project analyzes PCOS from three perspectives: medical records, Reddit patient discussions, and lifestyle behavior data. First, I cleaned the medical dataset and focused on observable symptoms such as menstrual irregularity, weight gain, hair growth, skin darkening, hair loss, and pimples. I calculated symptom prevalence among diagnosed PCOS patients and created charts to show which symptoms were most common. After, I collected r/PCOS Reddit posts using Python requests and Reddit’s public JSON endpoint. I used keyword matching to count how often the same symptom categories appeared in post titles and body text. I then compared the medical symptom percentages with Reddit discussion frequency using a grouped bar chart. I also trained 4 machine learning classifiers to test whether observable symptoms could predict PCOS diagnosis in the medical dataset. The models included Logistic Regression, Linear SVM, Random Forest, and XGBoost, and I evaluated them using accuracy, error, precision, recall, and F1-score. Finally, I analyzed lifestyle behavior factors from the lifestyle dataset, including stress level, exercise frequency, sweets intake, and fried food intake. These factors were analyzed separately from symptoms to provide additional context for PCOS management.

## Summary of Results

The results show that medical records and patient discussions partially overlap, but they do not emphasize PCOS symptoms in the same way.

- In the medical dataset, menstrual irregularity was the most common observable symptom among diagnosed PCOS patients.
- In r/PCOS Reddit posts, hair growth was the most discussed symptom, even though it was one of the least common symptoms in the medical dataset.
- The medical vs Reddit comparison suggests that some symptoms may carry more emotional or daily-life weight for patients than their medical prevalence alone shows.
- Classifier models showed that observable symptoms can help predict PCOS diagnosis in the medical dataset.
- XGBoost had the strongest overall model performance, while Random Forest provided a clear feature-importance ranking.
- Tree-based models identified skin darkening and hair growth as important predictors.
- The lifestyle analysis showed that people with PCOS had higher normalized scores for stress, sweets intake, and fried food intake, while exercise frequency was slightly lower.

Overall, the project shows that PCOS is better understood by combining medical data, patient experiences, and lifestyle context.

## How to run 
No API keys are required to run this project. 
Reddit posts are fetched automatically from r/PCOS using Python `requests`.

1. Install required Python packages using:

From the project root directory, run:

```bash
pip install -r requirements.txt
```
Required libraries include:
- requests
- pandas
- matplotlib
- scipy
- scikit-learn
- xgboost
- python-dotenv # loads environment variables from a `.env` file if needed
- jupyter

2. Download the Kaggle medical and lifestyle datasets locally

Kaggle CSV files are not included in this repository because the final project instructions prohibit uploading data files. To run the project, download the medical and lifestyle datasets from Kaggle and place them in a local data/ folder.

Expected local files:

data/PCOS_data.csv
data/diet_exercise_PCOSinsights.csv

3. Run the main pipeline: 

From the project root directory, run:

```bash
python src/main.py
```
Generated charts will appear in the `src/results/` folder. 

The primary project workflow is run through `src/main.py`. The notebook is included only as an optional interactive visualization layer that calls existing functions from the `src/` modules. Individual modules can also be run from the src/ directory if needed, but main.py is the primary entry point.

4. Open `results.ipynb` to view the analysis and visualizations.

5. Optional environmental file 
A .env.example file is included as a template.

To run tests:

```bash
python src/tests.py
```

## AI generated:
This project was developed with assistance from generative AI tools, including ChatGPT by OpenAI. As a beginner in Python, I used these tools to help me understand code, organize the project structure, debug errors, and implement parts of the data collection and analysis process. AI was used primarily as a learning aid to support my understanding of programming and data analysis concepts. All AI-generated code sections are clearly labeled in the source files with the comment `# AI generated:`. 

I made a sincere effort to understand each part of this project and connect the work back to the concepts taught throughout the course lectures. 

### PCOS care needs data, context, and empathy.

Thank you for your time! 

**Andrea Fernandez Cruz**  
USC Communication Data Science Graduate Student
University of Southern California  
Spring 2026