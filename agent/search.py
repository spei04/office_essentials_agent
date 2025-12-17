"""
Product search logic and coordination across vendors.
"""

from typing import List, Optional
from agent.schemas import SearchQuery, SearchResult, Product, Vendor
from integrations.base import VendorInterface


class ProductSearcher:
    """Coordinates product searches across multiple vendors."""
    
    def __init__(self, vendors: Optional[List[VendorInterface]] = None):
        """
        Initialize the product searcher.
        
        Args:
            vendors: List of vendor interfaces to search. If None, will be loaded dynamically.
        """
        self.vendors = vendors or []
    
    def register_vendor(self, vendor: VendorInterface):
        """Register a vendor for searching."""
        self.vendors.append(vendor)
    
    def search(self, query: SearchQuery) -> SearchResult:
        """
        Search for products across all registered vendors.
        
        Args:
            query: The search query
            
        Returns:
            SearchResult containing products from all vendors
        """
        all_products = []
        
        for vendor in self.vendors:
            try:
                products = vendor.search(query.query, max_results=query.max_results)
                all_products.extend(products)
            except Exception as e:
                # Log error but continue with other vendors
                print(f"Error searching vendor {vendor.get_name()}: {e}")
                continue
        
        # Filter by price if specified
        if query.min_price is not None:
            all_products = [p for p in all_products if p.price >= query.min_price]
        if query.max_price is not None:
            all_products = [p for p in all_products if p.price <= query.max_price]
        
        # Filter by preferred vendors if specified
        if query.preferred_vendors:
            all_products = [p for p in all_products if p.vendor in query.preferred_vendors]
        
        return SearchResult(
            query=query.query,
            products=all_products,
            total_found=len(all_products),
        )
    
    def search_multiple(self, queries: List[SearchQuery]) -> List[SearchResult]:
        """
        Execute multiple search queries.
        
        Args:
            queries: List of search queries
            
        Returns:
            List of search results
        """
        return [self.search(query) for query in queries]

