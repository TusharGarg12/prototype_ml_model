from fastapi import APIRouter, Query, HTTPException
from datetime import datetime
from typing import Optional
from models.schemas import ForecastResponse, ActualAttendanceFeedback, RetrainResponse
from core.forecasting import predict_headcount, reload_model
from core.train_model import train
import pandas as pd
import os

router = APIRouter()

@router.get("/headcount", response_model=ForecastResponse)
def get_headcount_forecast(
    date: str = Query(..., description="Forecast date in YYYY-MM-DD format"),
    meal_slot: str = Query(..., description="Meal slot: breakfast | lunch | dinner"),
    total_students: int = Query(600, description="Total registered students in this mess"),
    academic_event: Optional[str] = Query(None, description="Academic event: exam | holiday | fest | pre_holiday | post_holiday"),
    is_raining: bool = Query(False, description="Whether it is raining today"),
):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    day_of_week = date_obj.weekday()   # 0=Mon … 6=Sun
    month       = date_obj.month

    headcount, occupancy_pct, factors, confidence = predict_headcount(
        meal_type=meal_slot,
        day_of_week=day_of_week,
        total_students=total_students,
        academic_events=academic_event,
        is_raining=is_raining,
        month=month,
    )

    return ForecastResponse(
        date=date,
        meal_slot=meal_slot,
        total_students=total_students,
        expected_headcount=headcount,
        occupancy_percentage=occupancy_pct,
        confidence_level=confidence,
        determining_factors=factors,
    )

@router.post("/feedback")
def submit_actual_attendance(data: ActualAttendanceFeedback):
    """
    Receives actual attendance figures after a meal and appends them
    to our mock_attendance.csv dataset to enable continuous learning.
    """
    csv_path = "data/mock_attendance.csv"
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=500, detail="Historical dataset not found.")

    try:
        date_obj = datetime.strptime(data.date, "%Y-%m-%d")
        day_of_week = date_obj.weekday()
        month = date_obj.month
        
        # Calculate the actual percentage occupancy
        attendance_pct = data.actual_headcount / data.total_students
        attendance_pct = max(0.01, min(1.0, attendance_pct))
        
        # Create a new record matching our dataset format
        # We don't have scenario string for new data easily available, so we use 'baseline' 
        # or calculate it. We'll just leave scenario as 'actual_data' 
        new_record = {
            "date": data.date,
            "day_of_week": day_of_week,
            "month": month,
            "meal_slot": data.meal_slot.lower(),
            "scenario": "actual_data", # Placeholder for actual live data
            "academic_event": data.academic_event,
            "is_raining": int(data.is_raining),
            "attendance_pct": round(attendance_pct, 4),
            "actual_attendance": data.actual_headcount
        }
        
        df = pd.DataFrame([new_record])
        df.to_csv(csv_path, mode='a', header=False, index=False)
        
        return {"success": True, "message": "Actual attendance saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save feedback: {str(e)}")

@router.post("/retrain", response_model=RetrainResponse)
def trigger_model_retrain():
    """
    Triggers the XGBoost training script to learn from newly appended feedback data,
    then hot-reloads the model in memory.
    """
    try:
        # 1. Train the model
        report = train()
        if not report:
            return RetrainResponse(success=False, message="Training failed.")
            
        # 2. Reload the model into the forecasting module
        success, msg = reload_model()
        if not success:
            return RetrainResponse(success=False, message=f"Training succeeded but reload failed: {msg}")
            
        return RetrainResponse(
            success=True,
            message="Model successfully retrained and hot-reloaded.",
            mae_pct=report.get("mae_pct"),
            rmse_pct=report.get("rmse_pct"),
            r2_score=report.get("r2")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrain failed: {str(e)}")
