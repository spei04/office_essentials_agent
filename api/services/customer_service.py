"""
Customer service for business logic.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from api.models.customer import Customer
from api.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    """Service for customer operations."""
    
    @staticmethod
    def create_customer(db: Session, customer_data: CustomerCreate) -> Customer:
        """
        Create a new customer.
        
        Args:
            db: Database session
            customer_data: Customer data
            
        Returns:
            Created customer
        """
        customer = Customer(**customer_data.model_dump())
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer
    
    @staticmethod
    def get_customer(db: Session, customer_id: int) -> Optional[Customer]:
        """
        Get customer by ID.
        
        Args:
            db: Database session
            customer_id: Customer ID
            
        Returns:
            Customer or None
        """
        return db.query(Customer).filter(Customer.id == customer_id).first()
    
    @staticmethod
    def get_customer_by_email(db: Session, email: str) -> Optional[Customer]:
        """
        Get customer by email.
        
        Args:
            db: Database session
            email: Customer email
            
        Returns:
            Customer or None
        """
        return db.query(Customer).filter(Customer.email == email).first()
    
    @staticmethod
    def list_customers(db: Session, skip: int = 0, limit: int = 100) -> List[Customer]:
        """
        List all customers.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of customers
        """
        return db.query(Customer).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_customer(
        db: Session, customer_id: int, customer_data: CustomerUpdate
    ) -> Optional[Customer]:
        """
        Update a customer.
        
        Args:
            db: Database session
            customer_id: Customer ID
            customer_data: Updated customer data
            
        Returns:
            Updated customer or None
        """
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            return None
        
        update_data = customer_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(customer, field, value)
        
        db.commit()
        db.refresh(customer)
        return customer
    
    @staticmethod
    def delete_customer(db: Session, customer_id: int) -> bool:
        """
        Delete a customer.
        
        Args:
            db: Database session
            customer_id: Customer ID
            
        Returns:
            True if deleted, False if not found
        """
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            return False
        
        db.delete(customer)
        db.commit()
        return True

