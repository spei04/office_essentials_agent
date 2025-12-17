"""
External vendor and system integrations.
"""

from integrations.base import VendorInterface
from integrations.mock_vendor import MockVendor

__all__ = ["VendorInterface", "MockVendor"]

