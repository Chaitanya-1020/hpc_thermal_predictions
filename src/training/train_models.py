"""
Train multiple ML models for CPU temperature prediction.
"""
import math
from pathlib import Path
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.ensemble import RandomForestRegressor

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor


# --------------------------------------------------
# Paths
# --------------------------------------------------

DATASET = Path("data/processed/training_dataset.csv")

MODELS_DIR = Path("models")
REPORTS_DIR = Path("reports")

MODELS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

print("=" * 70)
print("MODEL TRAINING")
print("=" * 70)

df = pd.read_csv(DATASET)

print(f"\nDataset Shape : {df.shape}")


# --------------------------------------------------
# Prepare Features
# --------------------------------------------------

# ----------------------------------------
# Drop timestamp
# ----------------------------------------

df = df.drop(columns=["timestamp"])

# One-hot encode node

df = pd.get_dummies(df, columns=["node"], drop_first=True)

TARGET = "target_temperature"

X = df.drop(columns=[TARGET])

y = df[TARGET]

# ----------------------------------------
# Convert all features to numeric
# ----------------------------------------

X = X.apply(pd.to_numeric, errors="coerce")

# Replace inf values
X = X.replace([float("inf"), float("-inf")], float("nan"))

# Drop rows with NaN
valid_rows = X.notna().all(axis=1)

X = X.loc[valid_rows]

y = y.loc[valid_rows]

# Convert dtypes
X = X.astype("float32")

y = y.astype("float32")

print("\nFeature Types")

print(X.dtypes.value_counts())

# --------------------------------------------------
# Train Test Split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
)

print(f"Training Samples : {len(X_train)}")
print(f"Testing Samples  : {len(X_test)}")


# --------------------------------------------------
# Models
# --------------------------------------------------

models = {

    "RandomForest": RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
    ),

    "XGBoost": XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        random_state=42,
        objective="reg:squarederror",
    ),

    "LightGBM": LGBMRegressor(
    objective="regression",
    boosting_type="gbdt",
    n_estimators=300,
    learning_rate=0.05,
    max_depth=8,
    num_leaves=31,
    min_child_samples=20,
    random_state=42,
    verbosity=-1,
),
}


results = []

best_model = None
best_name = None
best_r2 = float("-inf")


# --------------------------------------------------
# Training Loop
# --------------------------------------------------

for name, model in models.items():

    print(f"\n{'='*60}")
    print(f"Training {name}")
    print("="*60)

    try:

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)

        mse = mean_squared_error(y_test, predictions)

        rmse = math.sqrt(mse)

        r2 = r2_score(y_test, predictions)

        print(f"MAE  : {mae:.4f}")
        print(f"RMSE : {rmse:.4f}")
        print(f"R²   : {r2:.4f}")

        results.append(
            {
                "Model": name,
                "MAE": mae,
                "RMSE": rmse,
                "R2": r2,
            }
        )

        if r2 > best_r2:
            best_r2 = r2
            best_model = model
            best_name = name

    except Exception as e:

        print(f"❌ {name} failed")

        print(e)

        continue
# --------------------------------------------------
# Save Report
# --------------------------------------------------

results_df = pd.DataFrame(results)

results_df.to_csv(
    REPORTS_DIR / "model_results.csv",
    index=False,
)


# --------------------------------------------------
# Save Best Model
# --------------------------------------------------

joblib.dump(
    best_model,
    MODELS_DIR / "best_model.pkl",
)

print("\n" + "=" * 70)
print("TRAINING COMPLETE")
print("=" * 70)

print(f"\nBest Model : {best_name}")
print(f"Best R²    : {best_r2:.4f}")

print("\nSaved Files")

print("models/best_model.pkl")
print("reports/model_results.csv")
import json
import joblib
# -------------------------------------
# Save Feature Columns
# -------------------------------------

joblib.dump(
    list(X.columns),
    MODELS_DIR / "feature_columns.pkl"
)

# -------------------------------------
# Save Metadata
# -------------------------------------

metadata = {
    "best_model": best_name,
    "r2": float(best_r2),
    "training_rows": int(len(X_train)),
    "testing_rows": int(len(X_test)),
    "feature_count": len(X.columns)
}

with open(
    MODELS_DIR / "metadata.json",
    "w"
) as f:

    json.dump(
        metadata,
        f,
        indent=4
    )