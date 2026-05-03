from fastapi import APIRouter
from models.schemas import SurgeRequest, SurgeResponse, WasteRequest, WasteResponse
from core.optimization.surge import calculate_surge_recommendations
from core.optimization.waste import calculate_batch_sizes

router = APIRouter()

@router.post("/surge", response_model=SurgeResponse)
def get_surge_recommendations(data: SurgeRequest):
    """
    Analyzes forecasted headcount and recommends 'Happy Hour' reward slots
    to shift traffic from peak to off-peak times.
    """
    result = calculate_surge_recommendations(
        meal_slot=data.meal_slot,
        expected_headcount=data.expected_headcount,
        total_capacity=data.total_capacity
    )
    
    return SurgeResponse(
        is_surge_expected=result["is_surge_expected"],
        peak_window=result["peak_window"],
        recommended_reward_slots=result["recommended_reward_slots"],
        analysis=result["analysis"]
    )

@router.post("/waste", response_model=WasteResponse)
def get_waste_optimization(data: WasteRequest):
    """
    Predicts required raw material quantities and suggests optimal 3-stage 
    batch cooking sizes to minimize end-of-service food waste.
    """
    result = calculate_batch_sizes(
        expected_headcount=data.expected_headcount,
        menu_items=data.menu_items
    )
    
    return WasteResponse(
        forecasted_headcount=result["forecasted_headcount"],
        planned_headcount_with_buffer=result["planned_headcount_with_buffer"],
        item_recommendations=result["item_recommendations"],
        estimated_waste_saved=result["estimated_waste_saved"],
        insight=result["insight"]
    )
