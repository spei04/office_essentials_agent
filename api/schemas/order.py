"""
Order schemas.
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from api.models.order import OrderStatus


class OrderItemResponse(BaseModel):
    """Order item response schema."""
    id: int
    item_name: str
    requested_quantity: int
    product_name: Optional[str] = None
    vendor: Optional[str] = None
    price: Optional[float] = None
    quantity_purchased: int
    status: str
    
    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """Order response schema."""
    id: int
    customer_id: int
    status: str
    total_amount: float
    budget_limit: Optional[float] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    """Schema for updating order status."""
    status: OrderStatus
    notes: Optional[str] = None

