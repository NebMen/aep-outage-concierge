from src.data_loader import LABOR_RATES, INDIRECT_LABOR_MULTIPLIER

def calculate_restoration_time(damaged_assets):
    """
    Calculates a restoration time range based on an array of damaged asset strings.
    """
    total_base_hours = 0.0
    
    for asset in damaged_assets:
        # Default to 1.0 hour if the asset isn't perfectly mapped in our dict
        total_base_hours += LABOR_RATES.get(asset, 1.0)
        
    # Apply the utility's mandatory operational multiplier
    estimated_hours = total_base_hours * INDIRECT_LABOR_MULTIPLIER
    
    # Create a realistic confidence interval (+/- 15%)
    min_time = round(estimated_hours * 0.85, 1)
    max_time = round(estimated_hours * 1.15, 1)
    
    return f"{min_time} - {max_time} hours"