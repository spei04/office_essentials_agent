"""
Order item model.
"""

from sqlalchemy import Column, String, Float, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from api.models.base import BaseModel


class OrderItem(BaseModel):
    """Order item model."""
    
    __tablename__ = "order_items"
    
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    item_name = Column(String(255), nullable=False)
    requested_quantity = Column(Integer, default=1)
    product_id = Column(String(255), nullable=True)  # Vendor product ID
    product_name = Column(String(500), nullable=True)
    vendor = Column(String(50), nullable=True)
    price = Column(Float, nullable=True)
    quantity_purchased = Column(Integer, default=0)
    status = Column(String(50), default="pending")
    notes = Column(Text, nullable=True)
    
    # Relationships
    order = relationship("Order", back_populates="items")

