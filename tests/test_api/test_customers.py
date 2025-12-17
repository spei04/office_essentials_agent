"""
Tests for customer endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.database import SessionLocal, Base, engine

# Create test database
Base.metadata.create_all(bind=engine)

client = TestClient(app)


@pytest.fixture
def db():
    """Database session fixture."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_customer():
    """Test creating a customer."""
    customer_data = {
        "name": "Test User",
        "email": "test@example.com",
        "company": "Test Company",
    }
    response = client.post("/api/v1/customers/", json=customer_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == customer_data["name"]
    assert data["email"] == customer_data["email"]


def test_list_customers():
    """Test listing customers."""
    response = client.get("/api/v1/customers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

