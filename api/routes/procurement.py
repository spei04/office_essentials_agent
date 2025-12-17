"""
Procurement routes.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from api.database import get_db
from api.schemas.procurement import ProcurementRequest, ProcurementResponse
from api.services.procurement_service import ProcurementService
from api.services.customer_service import CustomerService
from datetime import datetime

router = APIRouter()
procurement_service = ProcurementService()


@router.post("/", response_model=ProcurementResponse)
async def create_procurement_request(
    request: ProcurementRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Create a new procurement request."""
    # Verify customer exists
    customer = CustomerService.get_customer(db, request.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Create order first
    from api.services.order_service import OrderService
    order = OrderService.create_order(
        db=db,
        customer_id=request.customer_id,
        items=request.items,
        budget_limit=request.budget_limit,
        notes=request.notes,
    )
    
    # Process procurement in background
    background_tasks.add_task(
        procurement_service.process_procurement_async,
        order.id,
        request
    )
    
    return ProcurementResponse(
        order_id=order.id,
        status=order.status.value,
        message="Procurement request created and processing",
        created_at=order.created_at,
    )

