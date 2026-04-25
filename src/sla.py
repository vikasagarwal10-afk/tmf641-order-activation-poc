from datetime import datetime

# Simple SLA prediction based on product type
# In production, this would use ML models trained on historical data
def predict_sla_seconds(product_id: str, quantity: int) -> int:
    """Predict activation SLA in seconds"""
    
    # Simple mapping for POC
    sla_map = {
        "prepaid_mobile": 2,      # 2 seconds
        "postpaid_mobile": 5,      # 5 seconds
        "home_broadband": 30,      # 30 seconds
        "5g_slicing_gaming": 10,   # 10 seconds
        "iot_sensor": 15,          # 15 seconds
    }
    
    base_sla = sla_map.get(product_id, 60)  # default 60 seconds
    
    # Scale by quantity (non-linear for realism)
    import math
    scaled = base_sla * (1 + math.log(quantity) * 0.5)
    
    return int(scaled)

def calculate_actual_sla(created_at: datetime, activated_at: datetime) -> int:
    """Calculate actual SLA in seconds"""
    delta = activated_at - created_at
    return int(delta.total_seconds())