# 🔥 HPC Core Temperature Prediction using Machine Learning

A Machine Learning pipeline for predicting the **next 5-minute CPU core temperature** of High Performance Computing (HPC) nodes using telemetry data.

---

## 🚀 Features

- JSON telemetry ingestion
- MySQL database integration
- Data validation & preprocessing
- Feature engineering
- Model training & comparison
- Automatic best model selection
- Future temperature prediction
- Prediction storage in MySQL
- Prediction evaluation using actual telemetry

---

## 🛠 Tech Stack

- Python
- MySQL
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- LightGBM
- Joblib

---

## 📂 Project Structure

```text
TEMPERATURE_PROJECT/
│
├── data/
├── database/
├── models/
├── reports/
├── sample_data/
├── src/
│   ├── ingestion/
│   ├── preprocessing/
│   ├── feature_engineering/
│   ├── model_training/
│   └── inference/
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/Chaitanya-1020/TEMPERATURE_PROJECT.git

cd TEMPERATURE_PROJECT

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

---

## 🗄️ Database Setup

Create the database:

```sql
CREATE DATABASE hpc_thermal_prediction;
USE hpc_thermal_prediction;
```

Then execute:

```text
database/schema.sql
```

Update your MySQL credentials in:

```text
database/mysql_connection.py
```

---

## 📁 Dataset Structure

```text
data/raw/

├── cn21/
│   └── YYYY-MM-DD/
│       ├── temperature.json
│       ├── frequency.json
│       ├── cpu_usage.json
│       ├── power.json
│       └── energy.json
│
└── gpu45/
    └── YYYY-MM-DD/
        ├── temperature.json
        ├── frequency.json
        ├── cpu_usage.json
        ├── power.json
        └── energy.json
```

---

## ▶️ Run the Complete Pipeline

### 1. Data Ingestion

```bash
python -m src.ingestion.insert_temperature
python -m src.ingestion.insert_frequency
python -m src.ingestion.insert_cpu_usage
python -m src.ingestion.insert_power
python -m src.ingestion.insert_energy
```

### 2. Preprocessing

```bash
python -m src.preprocessing.validate_data
python -m src.preprocessing.merge_tables
python -m src.preprocessing.export_merged_dataset
```

### 3. Feature Engineering

```bash
python -m src.feature_engineering.feature_engineering
```

### 4. Train Model

```bash
python -m src.model_training.train_models
```

### 5. Predict Temperature

```bash
python -m src.inference.predict_temperature
```

### 6. Update Prediction Results (Optional)

```bash
python -m src.inference.update_prediction_results
```

---

## 🤖 Models

- Random Forest
- XGBoost ✅ Best Model
- LightGBM

**Evaluation Metrics**

- MAE
- RMSE
- R² Score

---

## 📊 Outputs

```text
data/processed/
├── merged_dataset.csv
└── training_dataset.csv

models/
├── best_model.pkl
├── feature_columns.pkl
└── metadata.json

reports/
└── model_results.csv

MySQL
└── temperature_predictions
```

---

## 🔄 Workflow

```text
Raw JSON
   │
   ▼
Data Ingestion
   │
   ▼
MySQL
   │
   ▼
Preprocessing
   │
   ▼
Feature Engineering
   │
   ▼
Model Training
   │
   ▼
Prediction
   │
   ▼
Store Predictions
   │
   ▼
Update with Actual Temperature
```

---

## 👨‍💻 Author

**Chaitanya Mule**
B.Tech Artificial Intelligence & Data Science

