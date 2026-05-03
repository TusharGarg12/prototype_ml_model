from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ForecastResponse(BaseModel):
    date: str = Field(..., description="Date of the forecast in YYYY-MM-DD format")
    meal_slot: str = Field(..., description="Meal slot: breakfast | lunch | dinner")
    total_students: int = Field(..., description="Total registered students in this mess")
    expected_headcount: int = Field(..., description="Predicted absolute headcount")
    occupancy_percentage: float = Field(..., description="Predicted occupancy as % of total_students")
    confidence_level: float = Field(..., description="Model confidence (0.0 - 1.0)")
    determining_factors: str = Field(..., description="Human-readable explanation of prediction drivers")

class ActualAttendanceFeedback(BaseModel):
    date: str = Field(..., description="Date of the meal in YYYY-MM-DD format")
    meal_slot: str = Field(..., description="Meal slot: breakfast | lunch | dinner")
    actual_headcount: int = Field(..., description="The real number of students who ate")
    total_students: int = Field(..., description="Total registered students in this mess")
    academic_event: Optional[str] = Field("None", description="Academic event: exam | holiday | fest | pre_holiday | post_holiday")
    is_raining: bool = Field(False, description="Whether it rained on this day")

class RetrainResponse(BaseModel):
    success: bool = Field(..., description="Whether training completed successfully")
    message: str = Field(..., description="Status message")
    mae_pct: Optional[float] = Field(None, description="Mean Absolute Error (Percentage)")
    rmse_pct: Optional[float] = Field(None, description="Root Mean Squared Error (Percentage)")
    r2_score: Optional[float] = Field(None, description="R2 Score")

class SurgeRequest(BaseModel):
    meal_slot: str = Field(..., description="Meal slot: breakfast | lunch | dinner")
    expected_headcount: int = Field(..., description="Expected headcount from ML forecast")
    total_capacity: int = Field(600, description="Total capacity of the mess")

class SurgeResponse(BaseModel):
    is_surge_expected: bool = Field(..., description="True if occupancy is high enough to cause congestion")
    peak_window: str = Field(..., description="The expected peak congestion time")
    recommended_reward_slots: List[Dict[str, str]] = Field(..., description="Suggested happy hour slots to shift traffic")
    analysis: str = Field(..., description="Text analysis of the situation")

class WasteRequest(BaseModel):
    expected_headcount: int = Field(..., description="Expected headcount from ML forecast")
    menu_items: List[str] = Field(..., description="List of menu items to be served")

class WasteResponse(BaseModel):
    forecasted_headcount: int = Field(..., description="Base forecast")
    planned_headcount_with_buffer: int = Field(..., description="Forecast + 10% safety buffer")
    item_recommendations: List[Dict[str, Any]] = Field(..., description="Batch sizing recommendations per item")
    estimated_waste_saved: str = Field(..., description="Estimate of food saved")
    insight: str = Field(..., description="Textual insight on the batching strategy")
