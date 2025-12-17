"""
Budget constraints and tracking.
"""

from typing import Optional


class BudgetPolicy:
    """Manages budget constraints for procurement."""
    
    def __init__(self, budget_limit: Optional[float] = None):
        """
        Initialize budget policy.
        
        Args:
            budget_limit: Maximum budget limit in USD
        """
        self.budget_limit = budget_limit
        self.spent = 0.0
    
    def check_budget(self, amount: float) -> tuple[bool, Optional[str]]:
        """
        Check if an amount is within budget.
        
        Args:
            amount: Amount to check
            
        Returns:
            Tuple of (is_within_budget, error_message)
        """
        if self.budget_limit is None:
            return True, None
        
        if self.spent + amount > self.budget_limit:
            return False, f"Purchase would exceed budget limit of ${self.budget_limit:.2f}"
        
        return True, None
    
    def record_purchase(self, amount: float):
        """
        Record a purchase against the budget.
        
        Args:
            amount: Amount spent
        """
        self.spent += amount
    
    def get_remaining_budget(self) -> Optional[float]:
        """
        Get remaining budget.
        
        Returns:
            Remaining budget or None if no limit
        """
        if self.budget_limit is None:
            return None
        return max(0, self.budget_limit - self.spent)
    
    def reset_budget(self):
        """Reset spent amount (e.g., for new budget period)."""
        self.spent = 0.0

