"""
Procurement service for orchestrating agent.
"""

import asyncio
from sqlalchemy.orm import Session
from typing import Optional
from api.models.order import Order, OrderStatus
from api.schemas.procurement import ProcurementRequest
from api.services.order_service import OrderService
from workflows.procure_office_essentials import procure_office_essentials
from agent.schemas import ProcurementRequest as AgentProcurementRequest, Vendor
from integrations.base import VendorInterface
from integrations.mock_vendor import MockVendor


class ProcurementService:
    """Service for procurement operations."""
    
    def __init__(self):
        """Initialize procurement service."""
        self.vendors: list[VendorInterface] = []
        self._initialize_vendors()
    
    def _initialize_vendors(self):
        """Initialize vendor integrations."""
        # For now, use mock vendor
        # In production, initialize real vendors based on config
        self.vendors.append(MockVendor())
    
    async     def process_procurement_async(
        self, order_id: int, request: ProcurementRequest
    ):
        """
        Process order asynchronously.
        
        Args:
            order_id: Order ID
            request: Procurement request
        """
        from api.database import SessionLocal
        db = SessionLocal()
        try:
            # Update status to processing
            order = OrderService.get_order(db, order_id)
            if order:
                order.status = OrderStatus.PROCESSING
                db.commit()
            
            # Convert to agent request
            preferred_vendors = None
            if request.preferred_vendors:
                preferred_vendors = [Vendor(v) for v in request.preferred_vendors]
            
            agent_request = AgentProcurementRequest(
                items=request.items,
                budget_limit=request.budget_limit,
                preferred_vendors=preferred_vendors,
                require_approval=False,  # Can be configured
            )
            
            # Run procurement workflow
            from policies.budget import BudgetPolicy
            from policies.approvals import ApprovalPolicy
            from api.config import settings
            
            budget_policy = BudgetPolicy(budget_limit=request.budget_limit)
            approval_policy = ApprovalPolicy(
                approval_threshold=settings.require_approval_above
            )
            
            purchase_result = procure_office_essentials(
                request=agent_request,
                vendors=self.vendors,
                budget_policy=budget_policy,
                approval_policy=approval_policy,
            )
            
            # Update order with results
            order = OrderService.get_order(db, order_id)
            if order:
                if purchase_result.success:
                    order.status = OrderStatus.COMPLETED
                    order.total_amount = purchase_result.total_cost
                else:
                    order.status = OrderStatus.FAILED
                    order.notes = purchase_result.error_message or "Purchase failed"
                
                db.commit()
        
        except Exception as e:
            # Update order status to failed
            order = OrderService.get_order(db, order_id)
            if order:
                order.status = OrderStatus.FAILED
                order.notes = f"Error: {str(e)}"
                db.commit()
        finally:
            db.close()

