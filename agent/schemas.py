"""
Data models and schemas for the office essentials procurement agent.
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class Vendor(str, Enum):
    """Supported vendors."""
    AMAZON = "amazon"
    STAPLES = "staples"
    COSTCO = "costco"
    MOCK = "mock"


class Product(BaseModel):
    """Product information."""
    id: str
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0, description="Price in USD")
    vendor: Vendor
    url: Optional[str] = None
    image_url: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    review_count: Optional[int] = Field(None, ge=0)
    in_stock: bool = True
    category: Optional[str] = None
    brand: Optional[str] = None


class SearchQuery(BaseModel):
    """Product search query."""
    query: str = Field(..., description="Search query string")
    category: Optional[str] = None
    max_results: int = Field(default=10, ge=1, le=50)
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    preferred_vendors: Optional[List[Vendor]] = None


class SearchResult(BaseModel):
    """Search result containing multiple products."""
    query: str
    products: List[Product]
    total_found: int
    search_time: datetime = Field(default_factory=datetime.now)


class OptimizationResult(BaseModel):
    """Result of price optimization."""
    selected_products: List[Product]
    total_cost: float
    savings: Optional[float] = None
    alternatives_considered: int
    optimization_time: datetime = Field(default_factory=datetime.now)


class PurchaseRequest(BaseModel):
    """Purchase request."""
    products: List[Product]
    total_amount: float
    requires_approval: bool = False
    notes: Optional[str] = None


class PurchaseResult(BaseModel):
    """Result of a purchase attempt."""
    success: bool
    order_id: Optional[str] = None
    products_purchased: List[Product]
    total_cost: float
    purchase_time: datetime = Field(default_factory=datetime.now)
    error_message: Optional[str] = None


class ProcurementRequest(BaseModel):
    """High-level procurement request."""
    items: List[str] = Field(..., description="List of items to procure (e.g., 'pens', 'paper')")
    budget_limit: Optional[float] = Field(None, ge=0)
    quantity_per_item: Optional[dict[str, int]] = None
    preferred_vendors: Optional[List[Vendor]] = None
    require_approval: bool = True

