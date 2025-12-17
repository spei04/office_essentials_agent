"""
Procurement request schemas.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class ProcurementRequest(BaseModel):
    """Schema for procurement request."""
    customer_id: int
    items: List[str] = Field(..., description="List of items to procure")
    budget_limit: Optional[float] = Field(None, ge=0, description="Budget limit in USD")
    quantity_per_item: Optional[Dict[str, int]] = Field(
        None, description="Quantity for each item"
    )
    preferred_vendors: Optional[List[str]] = None
    preferred_brands: Optional[List[str]] = None
    notes: Optional[str] = None


class ProcurementResponse(BaseModel):
    """Schema for procurement response."""
    order_id: int
    status: str
    message: str
    created_at: datetime
    
    class Config:
        from_attributes = True

