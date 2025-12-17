"""
Price optimization and product substitution logic.
"""

from typing import List, Optional
from agent.schemas import SearchResult, Product, OptimizationResult


class PriceOptimizer:
    """Optimizes product selection based on price and other factors."""
    
    def __init__(self):
        """Initialize the optimizer."""
        pass
    
    def optimize(self, search_results: List[SearchResult]) -> OptimizationResult:
        """
        Optimize product selection from search results.
        
        For each search query, selects the best product based on:
        - Price (lowest)
        - Availability (in stock)
        - Rating (if available)
        
        Args:
            search_results: List of search results to optimize
            
        Returns:
            OptimizationResult with selected products
        """
        selected_products = []
        alternatives_considered = 0
        
        for result in search_results:
            if not result.products:
                continue
            
            alternatives_considered += len(result.products)
            
            # Filter to in-stock products
            available_products = [p for p in result.products if p.in_stock]
            
            if not available_products:
                # If nothing in stock, use all products
                available_products = result.products
            
            # Sort by price (lowest first), then by rating (highest first)
            sorted_products = sorted(
                available_products,
                key=lambda p: (p.price, -(p.rating or 0))
            )
            
            # Select the best product
            best_product = sorted_products[0]
            selected_products.append(best_product)
        
        total_cost = sum(p.price for p in selected_products)
        
        return OptimizationResult(
            selected_products=selected_products,
            total_cost=total_cost,
            alternatives_considered=alternatives_considered,
        )
    
    def find_alternatives(self, product: Product, search_results: List[SearchResult]) -> List[Product]:
        """
        Find alternative products for a given product.
        
        Args:
            product: The product to find alternatives for
            search_results: Search results to look through
            
        Returns:
            List of alternative products
        """
        alternatives = []
        
        for result in search_results:
            for p in result.products:
                if p.id != product.id and p.vendor != product.vendor:
                    alternatives.append(p)
        
        # Sort by price
        alternatives.sort(key=lambda p: p.price)
        
        return alternatives

