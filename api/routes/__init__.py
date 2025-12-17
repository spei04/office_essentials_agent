"""
API routes.
"""

from fastapi import APIRouter
from api.routes import customers, procurement, orders, health

# Create main router
api_router = APIRouter()

# Include route modules
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(procurement.router, prefix="/procurement", tags=["procurement"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(health.router, prefix="/health", tags=["health"])

