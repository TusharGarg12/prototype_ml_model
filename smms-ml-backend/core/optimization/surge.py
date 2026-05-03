from typing import Dict, Any, List

def calculate_surge_recommendations(
    meal_slot: str, 
    expected_headcount: int, 
    total_capacity: int
) -> Dict[str, Any]:
    """
    Analyzes the expected headcount against the mess capacity and recommends
    dynamic 'Happy Hour' reward slots to shift peak traffic to off-peak times.
    """
    occupancy_rate = expected_headcount / total_capacity
    
    # Define standard dining windows for IIIT messes
    windows = {
        "breakfast": {"start": "07:30", "end": "09:30", "peak": "08:30 - 09:00"},
        "lunch": {"start": "12:00", "end": "14:00", "peak": "13:00 - 13:30"},
        "dinner": {"start": "19:30", "end": "21:30", "peak": "20:00 - 20:45"}
    }
    
    meal = meal_slot.lower()
    window = windows.get(meal, {"start": "12:00", "end": "14:00", "peak": "13:00 - 13:30"})
    
    response = {
        "is_surge_expected": False,
        "peak_window": window["peak"],
        "recommended_reward_slots": [],
        "analysis": ""
    }
    
    if occupancy_rate > 0.85:
        response["is_surge_expected"] = True
        response["analysis"] = f"Critical surge expected ({int(occupancy_rate*100)}% capacity). Severe congestion likely during {window['peak']}."
        response["recommended_reward_slots"] = [
            {
                "time_slot": f"{window['start']} - {window['start'][:3]}30", # e.g., 12:00 - 12:30
                "suggested_reward": "+50 points",
                "reasoning": "Incentivize early dining to pre-empt the surge."
            },
            {
                "time_slot": f"End of service (last 30 mins)", 
                "suggested_reward": "+75 points",
                "reasoning": "Strongest incentive needed to shift peak crowds to late dining."
            }
        ]
    elif occupancy_rate > 0.65:
        response["is_surge_expected"] = True
        response["analysis"] = f"Moderate surge expected ({int(occupancy_rate*100)}% capacity). Queue times will be slightly elevated."
        response["recommended_reward_slots"] = [
            {
                "time_slot": f"First 30 mins of service",
                "suggested_reward": "+20 points",
                "reasoning": "Mild incentive to flatten the curve."
            }
        ]
    else:
        response["analysis"] = f"Low traffic expected ({int(occupancy_rate*100)}% capacity). Normal operations are sufficient."
        
    return response
