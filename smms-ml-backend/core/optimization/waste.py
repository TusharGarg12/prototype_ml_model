from typing import Dict, Any, List
import math

# Baseline portion sizes in grams or ml per person
PORTION_SIZES = {
    "rice": 150,     # grams
    "dal": 200,      # ml
    "paneer": 150,   # grams
    "chicken": 200,  # grams
    "roti": 2,       # pieces (int)
    "curd": 100,     # ml
    "salad": 50,     # grams
    "dessert": 1     # piece/serving
}

def calculate_batch_sizes(
    expected_headcount: int, 
    menu_items: List[str]
) -> Dict[str, Any]:
    """
    Predicts required raw material quantities and suggests optimal batch cooking 
    sizes based on the ML forecasted headcount to minimize waste.
    """
    recommendations = []
    total_waste_saved_kg = 0.0
    
    # We assume a 10% safety buffer over the exact forecast to prevent shortages
    buffer_headcount = int(expected_headcount * 1.10)
    
    for item in menu_items:
        item_lower = item.lower()
        
        # Try to find a matching base portion size, default to 150g if unknown
        portion_size = 150
        unit = "g"
        for key in PORTION_SIZES:
            if key in item_lower:
                portion_size = PORTION_SIZES[key]
                if key in ["dal", "curd"]: unit = "ml"
                elif key in ["roti", "dessert"]: unit = "pieces"
                break
                
        # Calculate raw total required
        total_required = buffer_headcount * portion_size
        
        # Determine batching strategy
        if unit in ["g", "ml"]:
            # Convert to Kg / Liters
            total_kg_l = total_required / 1000.0
            
            # Suggest 3-batch cooking strategy (40%, 40%, 20% on-demand)
            batch_1 = round(total_kg_l * 0.40, 1)
            batch_2 = round(total_kg_l * 0.40, 1)
            batch_3 = round(total_kg_l * 0.20, 1)
            
            unit_display = "Kg" if unit == "g" else "Liters"
            
            recommendation = {
                "item": item,
                "total_required": f"{round(total_kg_l, 1)} {unit_display}",
                "batch_strategy": [
                    f"Batch 1 (Pre-service): {batch_1} {unit_display}",
                    f"Batch 2 (Mid-service): {batch_2} {unit_display}",
                    f"Batch 3 (On-Demand): {batch_3} {unit_display} (Cook only if crowd persists)"
                ]
            }
            # By reserving the last 20% to be cooked on-demand, we potentially save that amount from becoming waste.
            total_waste_saved_kg += batch_3
            
        else:
            # Discrete pieces (Roti, Dessert)
            batch_1 = int(total_required * 0.50)
            batch_2 = int(total_required * 0.50)
            
            recommendation = {
                "item": item,
                "total_required": f"{total_required} pieces",
                "batch_strategy": [
                    f"Batch 1: {batch_1} pieces",
                    f"Batch 2: {batch_2} pieces (Assess before preparing)"
                ]
            }
            
        recommendations.append(recommendation)

    # If the user over-cooks based on maximum capacity (e.g., 1000 students) instead of forecast (e.g. 700)
    # the waste would be massive. We estimate the AI's impact.
    
    return {
        "forecasted_headcount": expected_headcount,
        "planned_headcount_with_buffer": buffer_headcount,
        "item_recommendations": recommendations,
        "estimated_waste_saved": f"{round(total_waste_saved_kg, 1)} Kg/Liters of food saved via batching",
        "insight": "By utilizing a 3-stage batch cooking process tailored to the ML forecast, you significantly reduce end-of-service leftovers."
    }
