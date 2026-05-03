"""
generate_mock_data.py  –  SMMS ML Backend
==========================================
Generates a realistic 3-year (2024-2026) mess attendance dataset calibrated
against REAL survey responses collected from students via Google Form.

Survey baselines (absolute headcounts) encoded below:
  Baseline (Normal Wednesday): Breakfast=270, Lunch=380, Dinner=450
  Worst Menu (Tuesday):        Breakfast=230, Lunch=325, Dinner=380
  Best Menu (Sunday):          Breakfast=320, Lunch=480, Dinner=540
  Heavy Rain (Normal Day):     Breakfast=190, Lunch=320, Dinner=380
  Exam Week (Normal Weather):  Breakfast=390, Lunch=440, Dinner=520
  Fest Days (Effervescence):   Breakfast=130, Lunch=110, Dinner=220
  Normal Weekend (Saturday):   Breakfast=180, Lunch=420, Dinner=470
  Rain + Exam:                 Breakfast=350, Lunch=400, Dinner=440
  Rain + Weekend:              Breakfast=120, Lunch=360, Dinner=400
  Rain + Fest:                 Breakfast=150, Lunch=150, Dinner=250
  Flight Risk (Day Before Holiday): Breakfast=250, Lunch=250, Dinner=315
  Return Lag (Day After Holiday):   Breakfast=230, Lunch=325, Dinner=380

The total registered student count inferred from survey data is ~600
(Sunday best-case Dinner of 540 ≈ 90% turnout → 600 total students).
All predictions are stored as PERCENTAGE of total_students so the
model generalises to any mess size (multi-mess support).
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# ─────────────────────────────────────────────────────────────────
#  SURVEY-CALIBRATED BASELINES
#  Key: (meal, scenario_tag)  →  absolute headcount (out of ~600)
# ─────────────────────────────────────────────────────────────────
TOTAL_STUDENTS = 600          # Inferred from survey (Best-case Sunday dinner ≈ 90%)

SURVEY_BASELINES = {
    # (meal_slot, scenario) → attendance count
    ("breakfast", "baseline"):          270,
    ("lunch",     "baseline"):          380,
    ("dinner",    "baseline"):          450,

    ("breakfast", "worst_menu"):        230,
    ("lunch",     "worst_menu"):        325,
    ("dinner",    "worst_menu"):        380,

    ("breakfast", "best_menu"):         320,
    ("lunch",     "best_menu"):         480,
    ("dinner",    "best_menu"):         540,

    ("breakfast", "rain"):              190,
    ("lunch",     "rain"):              320,
    ("dinner",    "rain"):              380,

    ("breakfast", "exam"):              390,
    ("lunch",     "exam"):              440,
    ("dinner",    "exam"):              520,

    ("breakfast", "fest"):              130,
    ("lunch",     "fest"):              110,
    ("dinner",    "fest"):              220,

    ("breakfast", "weekend"):           180,
    ("lunch",     "weekend"):           420,
    ("dinner",    "weekend"):           470,

    ("breakfast", "rain_exam"):         350,
    ("lunch",     "rain_exam"):         400,
    ("dinner",    "rain_exam"):         440,

    ("breakfast", "rain_weekend"):      120,
    ("lunch",     "rain_weekend"):      360,
    ("dinner",    "rain_weekend"):      400,

    ("breakfast", "rain_fest"):         150,
    ("lunch",     "rain_fest"):         150,
    ("dinner",    "rain_fest"):         250,

    ("breakfast", "pre_holiday"):       250,
    ("lunch",     "pre_holiday"):       250,
    ("dinner",    "pre_holiday"):       315,

    ("breakfast", "post_holiday"):      230,
    ("lunch",     "post_holiday"):      325,
    ("dinner",    "post_holiday"):      380,
}

# Convert to percentage rates (normalised against TOTAL_STUDENTS)
BASELINE_RATES = {k: v / TOTAL_STUDENTS for k, v in SURVEY_BASELINES.items()}

# ─────────────────────────────────────────────────────────────────
#  ACADEMIC CALENDAR  (2024-2026)
# ─────────────────────────────────────────────────────────────────
def build_event_map():
    """
    Returns a dict  date_str → event_tag  covering 2024-2026.
    Tags: 'exam', 'holiday', 'fest', 'pre_holiday', 'post_holiday',
          'best_menu' (Sundays), 'rain' (monsoon months random days)
    """
    events = {}

    def tag(year, month, day, label):
        events[f"{year:04d}-{month:02d}-{day:02d}"] = label

    for year in [2024, 2025, 2026]:
        # National holidays
        tag(year,  1, 26, "holiday")   # Republic Day
        tag(year,  8, 15, "holiday")   # Independence Day
        tag(year, 10,  2, "holiday")   # Gandhi Jayanti
        tag(year, 12, 25, "holiday")   # Christmas

        # Pre- and post-holiday lag
        for m, d in [(1,25),(8,14),(10,1),(12,24)]:
            tag(year, m, d, "pre_holiday")
        for m, d in [(1,27),(8,16),(10,3),(12,26)]:
            tag(year, m, d, "post_holiday")

        # Mid-sem exams (Feb & Sep, 2 weeks each)
        for d in range(12, 23):
            tag(year, 2, d, "exam")
        for d in range(10, 21):
            tag(year, 9, d, "exam")

        # End-sem exams (Apr & Nov, 2 weeks each)
        for d in range(20, 31):
            tag(year, 4, d, "exam")
        for d in range(18, 30):
            tag(year, 11, d, "exam")

        # Summer vacation (May–Jul)  → treated as holiday (low occupancy)
        for month in [5, 6, 7]:
            for d in range(1, 32):
                try:
                    key = f"{year:04d}-{month:02d}-{d:02d}"
                    datetime.strptime(key, "%Y-%m-%d")
                    events[key] = "holiday"
                except ValueError:
                    pass

        # Winter break (mid-Dec onwards)
        for d in range(15, 32):
            try:
                key = f"{year:04d}-12-{d:02d}"
                datetime.strptime(key, "%Y-%m-%d")
                events[key] = "holiday"
            except ValueError:
                pass

        # College Fest – Effervescence (3rd week of March)
        for d in range(10, 14):
            tag(year, 3, d, "fest")

    return events


def resolve_scenario(date_obj, event_tag, is_raining):
    """
    Maps a day's properties to one of the survey scenario keys.
    Priority: rain combos > holiday variants > exam > fest > weekend > baseline
    """
    is_weekend = date_obj.weekday() >= 5   # Sat=5, Sun=6
    is_sunday  = date_obj.weekday() == 6

    if is_raining:
        if event_tag == "exam":       return "rain_exam"
        if event_tag in ("holiday",): return "rain_weekend"   # low occupancy
        if event_tag == "fest":       return "rain_fest"
        if is_weekend:                return "rain_weekend"
        return "rain"

    if event_tag == "pre_holiday":    return "pre_holiday"
    if event_tag == "post_holiday":   return "post_holiday"
    if event_tag in ("holiday",):     return "post_holiday"   # treat holiday like post
    if event_tag == "exam":           return "exam"
    if event_tag == "fest":           return "fest"
    if is_sunday:                     return "best_menu"       # Sunday best-menu effect
    if is_weekend:                    return "weekend"
    return "baseline"


def generate_mock_data(output_path="data/mock_attendance.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    event_map = build_event_map()

    # Monsoon months: Jun, Jul, Aug, Sep  → 40 % chance of rain on any day
    MONSOON_MONTHS = {6, 7, 8, 9}

    start_date = datetime(2024, 1, 1)
    end_date   = datetime(2026, 12, 31)
    total_days = (end_date - start_date).days + 1

    meals = ["breakfast", "lunch", "dinner"]
    records = []

    rng = np.random.default_rng(seed=42)

    print(f"Generating {total_days} days × {len(meals)} meals = "
          f"{total_days * len(meals)} records …")

    for i in range(total_days):
        date_obj  = start_date + timedelta(days=i)
        date_str  = date_obj.strftime("%Y-%m-%d")
        dow       = date_obj.weekday()          # 0=Mon … 6=Sun
        month     = date_obj.month

        # Stochastic rain flag
        rain_prob = 0.40 if month in MONSOON_MONTHS else 0.05
        is_raining = rng.random() < rain_prob

        event_tag = event_map.get(date_str, "normal")
        scenario  = resolve_scenario(date_obj, event_tag, is_raining)

        for meal in meals:
            key      = (meal, scenario)
            base_pct = BASELINE_RATES.get(key, BASELINE_RATES[(meal, "baseline")])

            # Gaussian noise ±8 % of base to simulate day-to-day variance
            noise = rng.normal(0, 0.08 * base_pct)
            pct   = float(np.clip(base_pct + noise, 0.05, 1.0))

            records.append({
                "date":              date_str,
                "day_of_week":       dow,
                "month":             month,
                "meal_slot":         meal,
                "scenario":          scenario,
                "academic_event":    event_tag if event_tag != "normal" else None,
                "is_raining":        int(is_raining),
                "attendance_pct":    round(pct, 4),      # ← target variable (percentage)
                "actual_attendance": int(round(pct * TOTAL_STUDENTS)),
            })

    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)

    print(f"Saved {len(df)} records to {output_path}")
    print("\nScenario distribution:")
    print(df["scenario"].value_counts().to_string())
    print(f"\nAttendance % stats:\n{df['attendance_pct'].describe().round(3).to_string()}")


if __name__ == "__main__":
    generate_mock_data()
