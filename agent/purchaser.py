"""
Final purchase decision and execution.
"""

from typing import Optional
from agent.schemas import OptimizationResult, PurchaseRequest, PurchaseResult, Product
from policies.budget import BudgetPolicy
from policies.approvals import ApprovalPolicy


class Purchaser:
    """Handles purchase decisions and execution."""
    
    def __init__(
        self,
        budget_policy: Optional[BudgetPolicy] = None,
        approval_policy: Optional[ApprovalPolicy] = None
    ):
        """
        Initialize the purchaser.
        
        Args:
            budget_policy: Budget policy to check against
            approval_policy: Approval policy to check against
        """
        self.budget_policy = budget_policy
        self.approval_policy = approval_policy
    
    def create_purchase_request(self, optimization_result: OptimizationResult) -> PurchaseRequest:
        """
        Create a purchase request from optimization results.
        
        Args:
            optimization_result: The optimization result
            
        Returns:
            PurchaseRequest ready for approval/execution
        """
        requires_approval = False
        
        if self.approval_policy:
            requires_approval = self.approval_policy.requires_approval(
                optimization_result.total_cost
            )
        
        return PurchaseRequest(
            products=optimization_result.selected_products,
            total_amount=optimization_result.total_cost,
            requires_approval=requires_approval,
        )
    
    def can_purchase(self, purchase_request: PurchaseRequest) -> tuple[bool, Optional[str]]:
        """
        Check if purchase can proceed.
        
        Args:
            purchase_request: The purchase request to check
            
        Returns:
            Tuple of (can_purchase, error_message)
        """
        # Check budget
        if self.budget_policy:
            can_afford, message = self.budget_policy.check_budget(purchase_request.total_amount)
            if not can_afford:
                return False, message
        
        # Check approval
        if purchase_request.requires_approval and self.approval_policy:
            approved = self.approval_policy.is_approved(purchase_request.total_amount)
            if not approved:
                return False, "Purchase requires approval"
        
        return True, None
    
    def execute_purchase(self, purchase_request: PurchaseRequest) -> PurchaseResult:
        """
        Execute a purchase (placeholder - actual implementation would call vendor APIs).
        
        Args:
            purchase_request: The purchase request to execute
            
        Returns:
            PurchaseResult indicating success or failure
        """
        can_purchase, error_message = self.can_purchase(purchase_request)
        
        if not can_purchase:
            return PurchaseResult(
                success=False,
                products_purchased=[],
                total_cost=purchase_request.total_amount,
                error_message=error_message,
            )
        
        # TODO: Implement actual purchase logic with vendor APIs
        # For now, return a mock success result
        return PurchaseResult(
            success=True,
            order_id="MOCK_ORDER_123",
            products_purchased=purchase_request.products,
            total_cost=purchase_request.total_amount,
        )

