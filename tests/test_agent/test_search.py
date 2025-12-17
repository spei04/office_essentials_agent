"""
Tests for product search functionality.
"""

import pytest
from agent.search import ProductSearcher
from agent.schemas import SearchQuery
from integrations.mock_vendor import MockVendor


def test_search_products():
    """Test searching for products."""
    searcher = ProductSearcher([MockVendor()])
    query = SearchQuery(query="pens", max_results=5)
    result = searcher.search(query)
    
    assert result.total_found > 0
    assert len(result.products) > 0
    assert result.query == "pens"


def test_search_multiple():
    """Test searching for multiple items."""
    searcher = ProductSearcher([MockVendor()])
    queries = [
        SearchQuery(query="pens"),
        SearchQuery(query="paper"),
    ]
    results = searcher.search_multiple(queries)
    
    assert len(results) == 2
    assert all(r.total_found > 0 for r in results)

