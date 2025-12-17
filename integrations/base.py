"""
Base vendor interface for all vendor integrations.
"""

from abc import ABC, abstractmethod
from typing import List
from agent.schemas import Product, Vendor


class VendorInterface(ABC):
    """Abstract base class for vendor integrations."""
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the vendor name."""
        pass
    
    @abstractmethod
    def get_vendor_type(self) -> Vendor:
        """Get the vendor type enum."""
        pass
    
    @abstractmethod
    def search(self, query: str, max_results: int = 10) -> List[Product]:
        """
        Search for products.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of Product objects
        """
        pass
    
    @abstractmethod
    def get_product(self, product_id: str) -> Product:
        """
        Get a specific product by ID.
        
        Args:
            product_id: The product ID
            
        Returns:
            Product object
        """
        pass
    
    @abstractmethod
    def purchase(self, product_id: str, quantity: int = 1) -> dict:
        """
        Purchase a product (placeholder - actual implementation varies by vendor).
        
        Args:
            product_id: The product ID to purchase
            quantity: Quantity to purchase
            
        Returns:
            Dictionary with purchase result (order_id, status, etc.)
        """
        pass

