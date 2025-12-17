"""
Main procurement workflow for office essentials.
"""

from agent.schemas import ProcurementRequest, PurchaseResult
from agent import Planner, ProductSearcher, PriceOptimizer, Purchaser
from policies import BudgetPolicy, ApprovalPolicy, PreferencesPolicy
from integrations.base import VendorInterface


def procure_office_essentials(
    request: ProcurementRequest,
    vendors: list[VendorInterface],
    budget_policy: BudgetPolicy | None = None,
    approval_policy: ApprovalPolicy | None = None,
    preferences_policy: PreferencesPolicy | None = None,
) -> PurchaseResult:
    """
    Main workflow for procuring office essentials.
    
    Args:
        request: The procurement request
        vendors: List of vendor interfaces to use
        budget_policy: Optional budget policy
        approval_policy: Optional approval policy
        preferences_policy: Optional preferences policy
        
    Returns:
        PurchaseResult indicating success or failure
    """
    # Initialize components
    planner = Planner()
    searcher = ProductSearcher(vendors)
    optimizer = PriceOptimizer()
    purchaser = Purchaser(budget_policy=budget_policy, approval_policy=approval_policy)
    
    # Step 1: Plan the procurement
    plan = planner.plan_procurement(request)
    search_queries = planner.create_search_queries(request)
    
    # Step 2: Search for products
    search_results = searcher.search_multiple(search_queries)
    
    # Step 3: Optimize product selection
    optimization_result = optimizer.optimize(search_results)
    
    # Step 4: Create purchase request
    purchase_request = purchaser.create_purchase_request(optimization_result)
    
    # Step 5: Execute purchase
    purchase_result = purchaser.execute_purchase(purchase_request)
    
    # Record purchase in budget if successful
    if purchase_result.success and budget_policy:
        budget_policy.record_purchase(purchase_result.total_cost)
    
    return purchase_result

