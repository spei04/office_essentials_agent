#!/usr/bin/env python3
"""
Seed database with sample data.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.database import SessionLocal
from api.models import Customer
from api.services.customer_service import CustomerService


def seed_data():
    """Seed database with sample data."""
    db = SessionLocal()
    
    try:
        # Create sample customers
        customers = [
            {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "company": "Acme Corp",
                "phone": "555-0101",
            },
            {
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "company": "Tech Solutions Inc",
                "phone": "555-0102",
            },
        ]
        
        for customer_data in customers:
            existing = CustomerService.get_customer_by_email(db, customer_data["email"])
            if not existing:
                CustomerService.create_customer(db, customer_data)
                print(f"Created customer: {customer_data['email']}")
            else:
                print(f"Customer already exists: {customer_data['email']}")
        
        print("Database seeded successfully!")
    
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()

