from fastapi import FastAPI, HTTPException, Header
from datetime import datetime
import uuid
import hashlib
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel

# ============ MODELS ============
class OrderItemAction(str, Enum):
    ADD = "add"
    MODIFY = "modify"
    DELETE = "delete"

class OrderItem(BaseModel):
    productId: str
    action: OrderItemAction
    quantity: int = 1

class OrderStatus(str, Enum):
    RECEIVED = "received"
    VALIDATED = "validated"
    IN_PROGRESS = "in_progress"
    ACTIVATED = "activated"
    FAILED = "failed"

class CustomerOrder(BaseModel):
    orderId: Optional[str] = None
    externalId: Optional[str] = None
    orderItem: List[OrderItem]
    status: OrderStatus = OrderStatus.RECEIVED
    createdAt: Optional[datetime] = None
    activatedAt: Optional[datetime] = None
    slaPredictedSeconds: Optional[int] = None
    slaActualSeconds: Optional[int] = None

class OrderResponse(BaseModel):
    orderId: str
    status: OrderStatus
    message: str
    slaPredictedSeconds: Optional[int] = None

# ============ IN-MEMORY STORAGE ============
orders_db = {}
idempotency_cache = {}

# ============ SLA PREDICTION ============
def predict_sla_seconds(product_id: str, quantity: int) -> int:
    sla_map = {
        "prepaid_mobile": 2,
        "postpaid_mobile": 5,
        "home_broadband": 30,
        "5g_slicing_gaming": 10,
        "iot_sensor": 15,
    }
    base_sla = sla_map.get(product_id, 60)
    import math
    scaled = base_sla * (1 + math.log(quantity) * 0.5)
    return int(scaled)

# ============ IDEMPOTENCY ============
def get_idempotency_key(request_id: str, subscriber_id: str) -> str:
    raw = f"{request_id}:{subscriber_id}"
    return hashlib.sha256(raw.encode()).hexdigest()

# ============ FASTAPI APP ============
app = FastAPI(
    title="TMF641 Order Management POC",
    description="POC for e& EA interview",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "TMF641 Order Management API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/order", response_model=OrderResponse)
async def create_order(
    order: CustomerOrder,
    x_request_id: Optional[str] = Header(None),
    x_subscriber_id: Optional[str] = Header(None)
):
    # Idempotency check
    if not x_request_id or not x_subscriber_id:
        raise HTTPException(status_code=400, detail="x-request-id and x-subscriber-id are required")
    
    idempotency_key = get_idempotency_key(x_request_id, x_subscriber_id)
    
    if idempotency_key in idempotency_cache:
        cached = idempotency_cache[idempotency_key]
        return OrderResponse(**cached)
    
    # Create order
    order_id = str(uuid.uuid4())
    order.orderId = order_id
    order.createdAt = datetime.now()
    
    first_item = order.orderItem[0]
    predicted_sla = predict_sla_seconds(first_item.productId, first_item.quantity)
    order.slaPredictedSeconds = predicted_sla
    
    # Store
    orders_db[order_id] = order
    
    # Simulate activation
    import asyncio
    await asyncio.sleep(0.5)
    
    activated_at = datetime.now()
    order.status = OrderStatus.ACTIVATED
    order.activatedAt = activated_at
    
    actual_sla = int((activated_at - order.createdAt).total_seconds())
    order.slaActualSeconds = actual_sla
    
    response_data = {
        "orderId": order_id,
        "status": OrderStatus.ACTIVATED,
        "message": f"Activated. Predicted: {predicted_sla}s, Actual: {actual_sla}s",
        "slaPredictedSeconds": predicted_sla
    }
    
    idempotency_cache[idempotency_key] = response_data
    
    return OrderResponse(**response_data)

@app.get("/order/{order_id}")
def get_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    order = orders_db[order_id]
    return {
        "orderId": order.orderId,
        "status": order.status,
        "createdAt": order.createdAt,
        "activatedAt": order.activatedAt,
        "slaPredictedSeconds": order.slaPredictedSeconds,
        "slaActualSeconds": order.slaActualSeconds
    }

@app.get("/orders")
def list_orders():
    """List all orders (for debugging)"""
    return {
        "count": len(orders_db),
        "orders": list(orders_db.keys())
    }