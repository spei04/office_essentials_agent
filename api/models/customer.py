"""
Customer model.
"""

from sqlalchemy import Column, String, Text
from api.models.base import BaseModel


class Customer(BaseModel):
    """Customer model."""
    
    __tablename__ = "customers"
    
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    company = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

