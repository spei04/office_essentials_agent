"""
High-level task planning and orchestration for procurement.
"""

from typing import List
from agent.schemas import ProcurementRequest, SearchQuery


class Planner:
    """Plans and orchestrates procurement tasks."""
    
    def __init__(self):
        """Initialize the planner."""
        pass
    
    def create_search_queries(self, request: ProcurementRequest) -> List[SearchQuery]:
        """
        Break down procurement request into search queries.
        
        Args:
            request: The procurement request
            
        Returns:
            List of search queries to execute
        """
        queries = []
        for item in request.items:
            query = SearchQuery(
                query=item,
                preferred_vendors=request.preferred_vendors,
            )
            queries.append(query)
        
        return queries
    
    def plan_procurement(self, request: ProcurementRequest) -> dict:
        """
        Create a procurement plan from a request.
        
        Args:
            request: The procurement request
            
        Returns:
            Dictionary containing the procurement plan
        """
        search_queries = self.create_search_queries(request)
        
        plan = {
            "items_to_procure": request.items,
            "search_queries": [q.query for q in search_queries],
            "budget_limit": request.budget_limit,
            "requires_approval": request.require_approval,
        }
        
        return plan

