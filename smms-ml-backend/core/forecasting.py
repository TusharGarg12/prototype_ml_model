"""
forecasting.py  –  SMMS ML Backend – Core Service
===================================================
Provides predict_headcount() which:
  1. Uses the trained XGBoost model if available (high confidence).
  2. Falls back to survey-calibrated heuristics (cold start).

The model predicts ATTENDANCE PERCENTAGE (0.0-1.0), making it
agnostic to individual mess sizes. The caller multiplies by
total_students to get the absolute headcount.
"""

from typing import Tuple
import os
import json
import warnings
import numpy as np

# ── Attempt to load model at module import time ───────────────────
MODEL_PATH   = "models/headcount_xgboost.json"
FEATURE_PATH = "models/feature_columns.json"
model           = None
feature_columns = None

try:
    import pandas as pd
    import xgboost as xgb

    if os.path.exists(MODEL_PATH) and os.path.exists(FEATURE_PATH):
        model = xgb.XGBRegressor()
        model.load_model(MODEL_PATH)
        with open(FEATURE_PATH) as f:
            feature_columns = json.load(f)
        print("[OK] XGBoost forecasting model loaded successfully.")
except ImportError:
    warnings.warn("pandas/xgboost unavailable - using heuristic fallback.")
except Exception as e:
    warnings.warn(f"Model load failed: {e} - using heuristic fallback.")

def reload_model():
    """
    Hot-reloads the XGBoost model from disk into memory.
    Called by the /retrain endpoint after continuous learning completes.
    """
    global model, feature_columns
    try:
        import xgboost as xgb
        if os.path.exists(MODEL_PATH) and os.path.exists(FEATURE_PATH):
            new_model = xgb.XGBRegressor()
            new_model.load_model(MODEL_PATH)
            with open(FEATURE_PATH) as f:
                new_features = json.load(f)
            
            # Atomic swap
            model = new_model
            feature_columns = new_features
            return True, "Model reloaded successfully in memory."
        return False, "Model files not found on disk."
    except Exception as e:
        return False, f"Failed to reload model: {e}"


# ── Survey-calibrated heuristic baselines (percentage) ───────────
# Derived from real Google Form survey responses (600 total students).
SURVEY_RATES = {
    ("breakfast", "baseline"):     270 / 600,
    ("lunch",     "baseline"):     380 / 600,
    ("dinner",    "baseline"):     450 / 600,
    ("breakfast", "exam"):         390 / 600,
    ("lunch",     "exam"):         440 / 600,
    ("dinner",    "exam"):         520 / 600,
    ("breakfast", "fest"):         130 / 600,
    ("lunch",     "fest"):         110 / 600,
    ("dinner",    "fest"):         220 / 600,
    ("breakfast", "weekend"):      180 / 600,
    ("lunch",     "weekend"):      420 / 600,
    ("dinner",    "weekend"):      470 / 600,
    ("breakfast", "rain"):         190 / 600,
    ("lunch",     "rain"):         320 / 600,
    ("dinner",    "rain"):         380 / 600,
    ("breakfast", "rain_exam"):    350 / 600,
    ("lunch",     "rain_exam"):    400 / 600,
    ("dinner",    "rain_exam"):    440 / 600,
    ("breakfast", "rain_weekend"): 120 / 600,
    ("lunch",     "rain_weekend"): 360 / 600,
    ("dinner",    "rain_weekend"): 400 / 600,
    ("breakfast", "rain_fest"):    150 / 600,
    ("lunch",     "rain_fest"):    150 / 600,
    ("dinner",    "rain_fest"):    250 / 600,
    ("breakfast", "pre_holiday"):  250 / 600,
    ("lunch",     "pre_holiday"):  250 / 600,
    ("dinner",    "pre_holiday"):  315 / 600,
    ("breakfast", "post_holiday"): 230 / 600,
    ("lunch",     "post_holiday"): 325 / 600,
    ("dinner",    "post_holiday"): 380 / 600,
    ("breakfast", "best_menu"):    320 / 600,
    ("lunch",     "best_menu"):    480 / 600,
    ("dinner",    "best_menu"):    540 / 600,
}


def _resolve_scenario(day_of_week: int, academic_event: str, is_raining: bool) -> str:
    """Map input signals to a survey scenario key."""
    is_weekend = day_of_week >= 5
    is_sunday  = day_of_week == 6
    ev = (academic_event or "").lower()

    if is_raining:
        if "exam"    in ev: return "rain_exam"
        if "fest"    in ev: return "rain_fest"
        if is_weekend:      return "rain_weekend"
        return "rain"

    if "pre_holiday"  in ev: return "pre_holiday"
    if "post_holiday" in ev: return "post_holiday"
    if "holiday"      in ev: return "post_holiday"
    if "exam"         in ev: return "exam"
    if "fest"         in ev: return "fest"
    if is_sunday:            return "best_menu"
    if is_weekend:           return "weekend"
    return "baseline"


def predict_headcount(
    meal_type:       str,
    day_of_week:     int,
    total_students:  int  = 600,
    academic_events: str  = None,
    is_raining:      bool = False,
    month:           int  = 6,
) -> Tuple[int, float, str, float]:
    """
    Predict mess headcount for a given meal slot.

    Args:
        meal_type       : 'breakfast' | 'lunch' | 'dinner'
        day_of_week     : 0 (Mon) – 6 (Sun)
        total_students  : Registered students in THIS mess (default 600)
        academic_events : Optional event string ('exam', 'holiday', 'fest', …)
        is_raining      : Weather flag
        month           : Calendar month (1-12) for seasonal patterns

    Returns:
        (expected_headcount, occupancy_pct, determining_factors, confidence)
    """
    meal_lower = meal_type.lower()
    scenario   = _resolve_scenario(day_of_week, academic_events, is_raining)

    # ─── ML Model branch ─────────────────────────────────────────
    if model is not None and feature_columns is not None:
        try:
            dow_sin   = float(np.sin(2 * np.pi * day_of_week / 7))
            dow_cos   = float(np.cos(2 * np.pi * day_of_week / 7))
            month_sin = float(np.sin(2 * np.pi * month / 12))
            month_cos = float(np.cos(2 * np.pi * month / 12))

            row = {
                "is_raining": int(is_raining),
                "dow_sin":    dow_sin,
                "dow_cos":    dow_cos,
                "month_sin":  month_sin,
                "month_cos":  month_cos,
            }
            # One-hot meal_slot
            for m in ["breakfast", "lunch", "dinner"]:
                row[f"meal_slot_{m}"] = int(meal_lower == m)
            # One-hot scenario
            for s in ["baseline","exam","fest","weekend","rain","rain_exam",
                       "rain_fest","rain_weekend","pre_holiday","post_holiday","best_menu"]:
                row[f"scenario_{s}"] = int(scenario == s)
            # One-hot academic_event
            for ev in ["None","exam","holiday","fest","pre_holiday","post_holiday","normal"]:
                row[f"academic_event_{ev}"] = int((academic_events or "None").lower() == ev.lower())

            df_input = pd.DataFrame([row])
            df_input = df_input.reindex(columns=feature_columns, fill_value=0)

            pct = float(model.predict(df_input)[0])
            pct = max(0.01, min(1.0, pct))

            headcount = int(round(pct * total_students))
            factors   = (f"XGBoost ML model | Scenario: {scenario} "
                         f"| {'Rain' if is_raining else 'No rain'} "
                         f"| {academic_events or 'No event'}")
            return headcount, round(pct * 100, 1), factors, 0.85

        except Exception as e:
            print(f"ML inference error: {e} — falling back to heuristic.")

    # ─── Survey-calibrated heuristic fallback ────────────────────
    base_pct = SURVEY_RATES.get((meal_lower, scenario),
               SURVEY_RATES.get((meal_lower, "baseline"), 0.60))

    headcount = int(round(base_pct * total_students))
    factors   = (f"Survey-calibrated heuristic | Scenario: {scenario} "
                 f"| {'Rain' if is_raining else 'No rain'} "
                 f"| {academic_events or 'No event'} (Cold Start Fallback)")
    return headcount, round(base_pct * 100, 1), factors, 0.45
