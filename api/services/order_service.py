"""
Order service for business logic.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from api.models.order import Order, OrderStatus
from api.schemas.order import OrderStatusUpdate


class OrderService:
    """Service for order operations."""
    
    @staticmethod
    def create_order(
        db: Session,
        customer_id: int,
        items: List[str],
        budget_limit: Optional[float] = None,
        notes: Optional[str] = None,
    ) -> Order:
        """
        Create a new order.
        
        Args:
            db: Database session
            customer_id: Customer ID
            items: List of item names
            budget_limit: Budget limit
            notes: Order notes
            
        Returns:
            Created order
        """
        from api.models.order_item import OrderItem
        
        order = Order(
            customer_id=customer_id,
            status=OrderStatus.PENDING,
            budget_limit=budget_limit,
            notes=notes,
        )
        db.add(order)
        db.flush()
        
        # Create order items
        for item_name in items:
            order_item = OrderItem(
                order_id=order.id,
                item_name=item_name,
                requested_quantity=1,
            )
            db.add(order_item)
        
        db.commit()
        db.refresh(order)
        return order
    
    @staticmethod
    def get_order(db: Session, order_id: int) -> Optional[Order]:
        """
        Get order by ID.
        
        Args:
            db: Database session
            order_id: Order ID
            
        Returns:
            Order or None
        """
        return db.query(Order).filter(Order.id == order_id).first()
    
    @staticmethod
    def list_orders(
        db: Session,
        customer_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Order]:
        """
        List orders.
        
        Args:
            db: Database session
            customer_id: Optional customer ID filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of orders
        """
        query = db.query(Order)
        if customer_id:
            query = query.filter(Order.customer_id == customer_id)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_order_status(
        db: Session, order_id: int, status_update: OrderStatusUpdate
    ) -> Optional[Order]:
        """
        Update order status.
        
        Args:
            db: Database session
            order_id: Order ID
            status_update: Status update data
            
        Returns:
            Updated order or None
        """
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return None
        
        order.status = status_update.status
        if status_update.notes:
            order.notes = status_update.notes
        
        db.commit()
        db.refresh(order)
        return order
    
    @staticmethod
    def update_order_total(db: Session, order_id: int, total_amount: float) -> Optional[Order]:
        """
        Update order total amount.
        
        Args:
            db: Database session
            order_id: Order ID
            total_amount: Total amount
            
        Returns:
            Updated order or None
        """
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return None
        
        order.total_amount = total_amount
        db.commit()
        db.refresh(order)
        return order

