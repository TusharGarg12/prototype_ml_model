"""
train_model.py  -  SMMS ML Backend
====================================
Trains an XGBoost Regressor to predict ATTENDANCE PERCENTAGE (0.0 - 1.0).
Because the model predicts a fraction rather than an absolute headcount,
the same model works for ANY mess regardless of total student count.

Usage:
    python core/train_model.py

Outputs:
    models/headcount_xgboost.json   - trained XGBoost model
    models/feature_columns.json     - ordered list of feature columns
    models/training_report.json     - evaluation metrics for traceability
"""

import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import os
import json

DATA_PATH    = "data/mock_attendance.csv"
MODEL_PATH   = "models/headcount_xgboost.json"
FEATURE_PATH = "models/feature_columns.json"
REPORT_PATH  = "models/training_report.json"


def train():
    if not os.path.exists(DATA_PATH):
        print(f"Dataset not found at {DATA_PATH}. "
              "Please run generate_mock_data.py first.")
        return False

    print("Loading dataset ...")
    df = pd.read_csv(DATA_PATH)

    # Feature engineering
    # Fill NaN academic event with 'None'
    df["academic_event"] = df["academic_event"].fillna("None")

    # Encode cyclic features: day_of_week and month as sin/cos pairs
    # so the model understands that Mon(0) and Sun(6) are close in cycle.
    df["dow_sin"]   = np.sin(2 * np.pi * df["day_of_week"] / 7)
    df["dow_cos"]   = np.cos(2 * np.pi * df["day_of_week"] / 7)
    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)

    # One-hot encode categorical columns
    cat_cols = ["meal_slot", "scenario", "academic_event"]
    df_encoded = pd.get_dummies(df, columns=cat_cols, drop_first=False)

    # Drop columns not used as features
    drop_cols = ["date", "actual_attendance", "attendance_pct",
                 "day_of_week", "month"]
    X = df_encoded.drop(columns=[c for c in drop_cols if c in df_encoded.columns])
    y = df["attendance_pct"]   # target: occupancy fraction (0.0 - 1.0)

    # Save ordered feature columns for inference alignment
    feature_columns = list(X.columns)
    os.makedirs("models", exist_ok=True)
    with open(FEATURE_PATH, "w") as f:
        json.dump(feature_columns, f, indent=2)

    # Train / test split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"Training on {len(X_train):,} samples | Evaluating on {len(X_test):,} samples")

    model = XGBRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=50)

    # Evaluation
    preds = model.predict(X_test)
    mae  = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2   = r2_score(y_test, preds)

    # Convert % errors to student counts (assuming 600 baseline)
    mae_students  = mae  * 600
    rmse_students = rmse * 600

    print("\n" + "=" * 50)
    print("  MODEL EVALUATION REPORT")
    print("=" * 50)
    print(f"  MAE  : {mae:.4f}  ({mae_students:.1f} students out of 600)")
    print(f"  RMSE : {rmse:.4f}  ({rmse_students:.1f} students out of 600)")
    print(f"  R2   : {r2:.4f}")
    print("=" * 50)

    # Save model
    model.save_model(MODEL_PATH)
    print(f"\nModel saved -> {MODEL_PATH}")

    # Save report for traceability
    report = {
        "training_samples":  len(X_train),
        "test_samples":      len(X_test),
        "total_samples":     len(X),
        "features":          len(feature_columns),
        "mae_pct":           round(mae, 6),
        "rmse_pct":          round(rmse, 6),
        "r2":                round(r2, 6),
        "mae_students_600":  round(mae_students, 1),
        "rmse_students_600": round(rmse_students, 1),
        "note": "Target is attendance_pct (0.0-1.0). "
                "Multiply by total_students for absolute headcount.",
    }
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Training report saved -> {REPORT_PATH}")

    # Feature importances (top 10)
    importances = pd.Series(
        model.feature_importances_, index=feature_columns
    ).sort_values(ascending=False)
    print("\nTop 10 Feature Importances:")
    print(importances.head(10).round(4).to_string())
    
    return report


if __name__ == "__main__":
    train()
