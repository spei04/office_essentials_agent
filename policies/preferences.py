"""
User and company preferences (vendors, brands, etc.).
"""

from typing import List, Optional
from agent.schemas import Vendor


class PreferencesPolicy:
    """Manages procurement preferences."""
    
    def __init__(
        self,
        preferred_vendors: Optional[List[Vendor]] = None,
        preferred_brands: Optional[List[str]] = None,
        excluded_vendors: Optional[List[Vendor]] = None,
        excluded_brands: Optional[List[str]] = None,
    ):
        """
        Initialize preferences policy.
        
        Args:
            preferred_vendors: List of preferred vendors (ordered by preference)
            preferred_brands: List of preferred brands
            excluded_vendors: List of vendors to exclude
            excluded_brands: List of brands to exclude
        """
        self.preferred_vendors = preferred_vendors or []
        self.preferred_brands = preferred_brands or []
        self.excluded_vendors = excluded_vendors or []
        self.excluded_brands = excluded_brands or []
    
    def is_vendor_preferred(self, vendor: Vendor) -> bool:
        """
        Check if a vendor is preferred.
        
        Args:
            vendor: Vendor to check
            
        Returns:
            True if vendor is preferred
        """
        return vendor in self.preferred_vendors
    
    def is_vendor_excluded(self, vendor: Vendor) -> bool:
        """
        Check if a vendor is excluded.
        
        Args:
            vendor: Vendor to check
            
        Returns:
            True if vendor is excluded
        """
        return vendor in self.excluded_vendors
    
    def is_brand_preferred(self, brand: Optional[str]) -> bool:
        """
        Check if a brand is preferred.
        
        Args:
            brand: Brand to check
            
        Returns:
            True if brand is preferred
        """
        if not brand:
            return False
        return brand.lower() in [b.lower() for b in self.preferred_brands]
    
    def is_brand_excluded(self, brand: Optional[str]) -> bool:
        """
        Check if a brand is excluded.
        
        Args:
            brand: Brand to check
            
        Returns:
            True if brand is excluded
        """
        if not brand:
            return False
        return brand.lower() in [b.lower() for b in self.excluded_brands]
    
    def get_vendor_preference_score(self, vendor: Vendor) -> int:
        """
        Get vendor preference score (lower is better).
        
        Args:
            vendor: Vendor to score
            
        Returns:
            Preference score (0 = most preferred, higher = less preferred)
        """
        if vendor in self.excluded_vendors:
            return 999
        
        if vendor in self.preferred_vendors:
            return self.preferred_vendors.index(vendor)
        
        return 100  # Neutral score for non-preferred, non-excluded vendors

