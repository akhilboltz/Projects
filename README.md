# 📄 Automated Resume Matching & Screening System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine_Learning-orange)
![XGBoost](https://img.shields.io/badge/XGBoost-Gradient_Boosting-green)
![NLTK](https://img.shields.io/badge/NLTK-NLP_Processing-yellow)

## 📖 Overview

This project implements an **End-to-End NLP Pipeline** designed to automate the initial screening phase of recruitment. By analyzing job applicant data and matching resumes to job descriptions, the system provides a scalable solution for ranking candidates based on relevance.

The solution leverages advanced text preprocessing, feature engineering, and ensemble machine learning models to classify candidates as a "Best Match" with high precision.

## 🎯 Key Achievements

* **Pipeline Engineering:** Built a robust text processing pipeline handling tokenization, stop-word removal, and lemmatization for unstructured text data.
* **Model Optimization:** Benchmarked Logistic Regression, Random Forest, and XGBoost, achieving **~89% accuracy** with an optimized XGBoost model.
* **Hyperparameter Tuning:** Implemented a two-stage tuning strategy using **RandomizedSearchCV** followed by **GridSearchCV** to maximize model performance.
* **Feature Engineering:** Utilized **CountVectorizer** (Bag of Words) to convert complex textual metadata (Resume, Job Description, Demographics) into actionable numerical vectors.

---

## 🛠️ Tech Stack

* **Language:** Python
* **NLP:** NLTK (Tokenization, Lemmatization, Stopwords), Gensim (Word2Vec exp.)
* **Machine Learning:** Scikit-Learn, XGBoost
* **Data Processing:** Pandas, NumPy
* **Visualization:** Matplotlib, Seaborn

---

## 📊 Methodology

### 1. Data Preprocessing & Cleaning
Raw textual data from resumes and job descriptions is unstructured and noisy. The pipeline cleans this data to ensure model interpretability:
* **Text Cleaning:** Lowercasing, punctuation removal, and tokenization.
* **Normalization:** Applied **WordNetLemmatizer** to reduce words to their root form (e.g., "running" $\rightarrow$ "run").
* **Noise Reduction:** Removed standard English stopwords to focus on semantic content.

### 2. Feature Engineering
The model inputs are not just text. I constructed a composite feature string `df_rec` combining:
`Gender` + `Ethnicity` + `Age` + `Resume Content` + `Job Description` + `Job Roles`.

This composite feature was transformed using **CountVectorizer (Max Features = 5000)** to create a sparse matrix representation suitable for machine learning.

### 3. Model Benchmarking
I evaluated three distinct classifiers to find the optimal balance of bias and variance:

| Model | Role | Outcome |
| :--- | :--- | :--- |
| **Logistic Regression** | Baseline | Good interpretability, lower accuracy. |
| **Random Forest** | Ensemble Bagging | Robust against overfitting. |
| **XGBoost (Winner)** | Ensemble Boosting | Best performance (~89% Acc) after tuning. |

---

## ⚙️ Optimization Strategy

To push the XGBoost model beyond default performance, I implemented a rigorous tuning process:

1.  **Coarse Search (RandomizedSearchCV):** Explored a wide distribution of parameters (Learning Rate, Max Depth, Subsample, N_Estimators).
2.  **Fine Search (GridSearchCV):** Narrowed down the search space around the best parameters found in step 1 to pinpoint the global minimum.

**Final Optimized Parameters:**
* *Learning Rate:* Tuned via linear space search.
* *Max Depth:* Controlled model complexity.
* *Subsample:* Prevented overfitting by training on partial data splits.

---

## 🚀 How to Run
1.  **Install dependencies:**
    ```bash
    pip install pandas numpy scikit-learn xgboost nltk gensim matplotlib seaborn
    ```

2.  **Download NLTK Data (First Run Only):**
    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    ```

3.  **Run the Script:**
    Execute the notebook or python script to preprocess data, train the model, and view the evaluation report.

