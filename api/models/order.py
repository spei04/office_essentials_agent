"""
Order model.
"""

from sqlalchemy import Column, String, Float, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from api.models.base import BaseModel
import enum


class OrderStatus(str, enum.Enum):
    """Order status enum."""
    PENDING = "pending"
    PROCESSING = "processing"
    SEARCHING = "searching"
    OPTIMIZING = "optimizing"
    PURCHASING = "purchasing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Order(BaseModel):
    """Order model."""
    
    __tablename__ = "orders"
    
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    total_amount = Column(Float, default=0.0)
    budget_limit = Column(Float, nullable=True)
    notes = Column(String(1000), nullable=True)
    
    # Relationships
    customer = relationship("Customer", backref="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

