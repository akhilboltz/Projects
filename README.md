# 🏭 Industrial CNC Tool Wear Prediction (Time-Series Forecasting)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.12%2B-orange)
![Optuna](https://img.shields.io/badge/Optuna-Hyperparameter_Tuning-lightgrey)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📖 Overview

This project implements an **End-to-End Deep Learning Pipeline** for Predictive Maintenance in an industrial setting. The goal is to estimate the wear (in microns) of CNC machine tools based on high-frequency sensor data (Vibration, Force, Acoustic Emission) in real-time.

Unlike standard time-series projects, this solution strictly addresses **Domain Shift** and **Data Leakage** by training on specific physical tools and testing on completely unseen hardware, simulating a real-world factory deployment scenario.

## 🎯 Key Achievements

* **Engineering Rigor:** Implemented **Leave-Group-Out Validation** to ensure zero temporal leakage between training and testing data.
* **Architecture Analysis:** Designed and benchmarked custom **LSTM** and **Transformer** architectures from scratch using TensorFlow/Keras Subclassing.
* **Optimization:** Reduced Validation MSE by **16x** using **Bayesian Optimization (Optuna)**.
* **Result:** Achieved a Mean Absolute Error (MAE) of **53.9 microns** on unseen test tools.

---

## 🛠️ Tech Stack

* **Deep Learning:** TensorFlow, Keras (Functional API & Custom Layers)
* **Optimization:** Optuna (Bayesian Hyperparameter Tuning), AdamW
* **Data Processing:** Pandas, NumPy, Scikit-Learn (StandardScaler)
* **Visualization:** Matplotlib, Seaborn

---

## 📊 Dataset & Preprocessing

The dataset consists of multi-sensor readings from CNC milling operations.
* **Input Features:** 50+ raw signals (Force, Vibration, Current, etc.) reduced to ~27 high-variance features.
* **Target:** `Vb` (Flank Wear) measured in microns.

### Data Engineering Strategy
1.  **Feature Selection:** Removed low-variance velocity columns and highly correlated (>0.95) redundant features using Correlation Heatmaps.
2.  **Sliding Window:** Generated time-series windows (Lookback = 50 steps) to capture temporal dependencies.
3.  **Strict Split Strategy:**
    * *Bad Practice:* Random Shuffle (Causes leakage).
    * *My Approach:* **Leave-Group-Out**. I trained on Tools #1-10 and tested on Tools #11-15. This forces the model to learn the *physics* of wear rather than memorizing a specific machine's noise.

---

## 🧠 Model Architectures

Two distinct architectures were developed to compare **Inductive Bias (LSTM)** vs. **Model Complexity (Transformer)**.

### 1. Custom LSTM Block
A sequential architecture designed to capture long-term dependencies in time-series data.
* **Structure:** Dual LSTM layers with varying units + Dropout + Dense Head.
* **Why:** LSTMs have a strong inductive bias for sequential data, making them robust for smaller datasets.

### 2. Multi-Head Self-Attention Transformer
A parallel architecture using Self-Attention mechanisms.
* **Structure:** Positional Embeddings + Multi-Head Attention + LayerNorm + Conv1D Feed-Forward Network.
* **Why:** Transformers excel at finding global relationships across the time window but typically require massive datasets.

---

## ⚙️ Optimization (Optuna)

Manual tuning was replaced with **Bayesian Hyperparameter Optimization** using `Optuna`. The search space included:
* **Units:** 16 - 128 (Step 16)
* **Dropout Rate:** 0.1 - 0.5
* **Learning Rate:** 1e-4 - 1e-2 (Log scale)
* **Weight Decay:** 1e-5 - 1e-2 (For regularization)

**Impact:** This process identified the optimal configuration that minimized validation loss while preventing overfitting via Early Stopping.

---

## 📉 Results & Evaluation

I conducted a direct "Shootout" between the optimized LSTM and the Transformer on the held-out Test Set.

| Model | MAE (Microns) | Observation |
| :--- | :--- | :--- |
| **LSTM (Winner)** | **54.69 µm** | Better at tracking sudden wear spikes in this dataset. |
| Transformer | 77.4 µm | Smoother predictions but slightly less reactive to local trends. |

**Conclusion:** For this specific industrial problem with limited samples (~1,000 windows), the simpler **LSTM** outperformed the complex Transformer, proving that *model complexity does not always equal better performance.*

---

## 🚀 How to Run
1.  **Install dependencies:**
    ```bash
    pip install pandas numpy tensorflow optuna matplotlib scikit-learn
    ```

3.  **Run the Notebook:**
    Open `main.ipynb` (or your notebook name) in Jupyter or Google Colab to see the full training and evaluation pipeline.

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
