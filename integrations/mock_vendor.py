"""
Mock vendor for testing without real API keys.
"""

from typing import List
from agent.schemas import Product, Vendor
from integrations.base import VendorInterface


class MockVendor(VendorInterface):
    """Mock vendor implementation for testing."""
    
    def __init__(self):
        """Initialize the mock vendor."""
        self._products = self._generate_mock_products()
    
    def get_name(self) -> str:
        """Get the vendor name."""
        return "Mock Vendor"
    
    def get_vendor_type(self) -> Vendor:
        """Get the vendor type."""
        return Vendor.MOCK
    
    def _generate_mock_products(self) -> List[Product]:
        """Generate mock products for testing."""
        return [
            Product(
                id="mock-1",
                name="Office Pens - Pack of 12",
                description="Black ballpoint pens",
                price=8.99,
                vendor=Vendor.MOCK,
                rating=4.5,
                review_count=120,
                in_stock=True,
                category="Office Supplies",
                brand="MockBrand",
            ),
            Product(
                id="mock-2",
                name="Copy Paper - 500 Sheets",
                description="White printer paper",
                price=6.99,
                vendor=Vendor.MOCK,
                rating=4.2,
                review_count=85,
                in_stock=True,
                category="Office Supplies",
                brand="MockBrand",
            ),
            Product(
                id="mock-3",
                name="Stapler - Heavy Duty",
                description="Metal stapler",
                price=12.99,
                vendor=Vendor.MOCK,
                rating=4.7,
                review_count=200,
                in_stock=True,
                category="Office Supplies",
                brand="MockBrand",
            ),
        ]
    
    def search(self, query: str, max_results: int = 10) -> List[Product]:
        """
        Search for products (mock implementation).
        
        Args:
            query: Search query string
            max_results: Maximum number of results
            
        Returns:
            List of matching products
        """
        query_lower = query.lower()
        matching = [
            p for p in self._products
            if query_lower in p.name.lower() or query_lower in (p.description or "").lower()
        ]
        return matching[:max_results]
    
    def get_product(self, product_id: str) -> Product:
        """
        Get a specific product by ID.
        
        Args:
            product_id: The product ID
            
        Returns:
            Product object
        """
        for product in self._products:
            if product.id == product_id:
                return product
        raise ValueError(f"Product {product_id} not found")
    
    def purchase(self, product_id: str, quantity: int = 1) -> dict:
        """
        Mock purchase implementation.
        
        Args:
            product_id: The product ID to purchase
            quantity: Quantity to purchase
            
        Returns:
            Dictionary with mock purchase result
        """
        product = self.get_product(product_id)
        return {
            "order_id": f"MOCK-ORDER-{product_id}-{quantity}",
            "status": "success",
            "product_id": product_id,
            "quantity": quantity,
            "total_cost": product.price * quantity,
        }

