from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

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
    externalId: Optional[str] None
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