# Office Essentials Procurement Agent - Project Structure

## Architecture Overview

- **Frontend Web App**: Customer-facing web interface (React/HTML)
- **API Backend**: FastAPI REST API for handling customer requests
- **Procurement Agent**: Backend service that processes procurement requests
- **AWS Deployment**: Containerized deployment on AWS (ECS/Lambda/EC2)

```
office_essentials_agent/
│
├── README.md                    # Project documentation
├── PROJECT_STRUCTURE.md         # This file
├── pyproject.toml               # Python project configuration
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── Dockerfile                   # Docker image for backend
├── docker-compose.yml           # Local development setup
│
├── frontend/                    # Web application frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.jsx              # Main React component
│   │   ├── components/
│   │   │   ├── ProcurementForm.jsx
│   │   │   ├── ProductList.jsx
│   │   │   └── OrderStatus.jsx
│   │   ├── services/
│   │   │   └── api.js           # API client
│   │   └── styles/
│   │       └── main.css
│   ├── package.json
│   └── Dockerfile               # Frontend Docker image
│
├── api/                         # FastAPI REST API
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── customers.py        # Customer management endpoints
│   │   ├── procurement.py     # Procurement request endpoints
│   │   └── orders.py           # Order status endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── customer.py         # Customer data models
│   │   └── order.py            # Order data models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── customer_service.py # Customer business logic
│   │   └── procurement_service.py  # Procurement orchestration
│   └── database/
│       ├── __init__.py
│       ├── connection.py       # Database connection
│       └── migrations/         # Database migrations
│
├── agent/                       # Core procurement agent
│   ├── __init__.py
│   ├── planner.py              # High-level task planning
│   ├── search.py               # Product search logic
│   ├── optimizer.py            # Price optimization
│   ├── purchaser.py            # Purchase execution
│   └── schemas.py              # Data models
│
├── integrations/                # External vendor integrations
│   ├── __init__.py
│   ├── base.py                 # Base vendor interface
│   ├── amazon.py               # Amazon API
│   ├── staples.py              # Staples API
│   ├── costco.py               # Costco API
│   └── mock_vendor.py          # Mock vendor for testing
│
├── policies/                    # Business rules
│   ├── __init__.py
│   ├── budget.py               # Budget constraints
│   ├── preferences.py          # User preferences
│   └── approvals.py            # Approval workflows
│
├── workflows/                   # End-to-end workflows
│   ├── __init__.py
│   └── procure_office_essentials.py
│
├── aws/                         # AWS deployment configurations
│   ├── cloudformation/
│   │   ├── infrastructure.yaml  # Infrastructure as code
│   │   └── api-gateway.yaml    # API Gateway config
│   ├── ecs/
│   │   ├── task-definition.json # ECS task definition
│   │   └── service-definition.json
│   ├── lambda/
│   │   └── procurement-handler.py  # Lambda function (optional)
│   └── scripts/
│       ├── deploy.sh            # Deployment script
│       └── setup.sh            # AWS setup script
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_api/
│   │   ├── test_customers.py
│   │   └── test_procurement.py
│   ├── test_agent/
│   │   ├── test_search.py
│   │   └── test_optimizer.py
│   └── fixtures/
│       └── sample_data.json
│
└── scripts/                     # Utility scripts
    ├── run_local.py            # Run locally
    └── setup_db.py             # Database setup
```

## Component Descriptions

### `/frontend`
Customer-facing web application built with React (or vanilla HTML/JS)
- Form for customers to input procurement requests
- Display order status and history
- Real-time updates via WebSocket or polling

### `/api`
FastAPI REST API backend
- Handles customer registration and authentication
- Accepts procurement requests from frontend
- Queues requests for agent processing
- Returns order status and results

### `/agent`
Core procurement intelligence (same as before)
- Processes procurement requests
- Searches, optimizes, and purchases products

### `/aws`
AWS deployment configurations
- CloudFormation templates for infrastructure
- ECS task definitions for containerized deployment
- Lambda functions (if using serverless)
- Deployment scripts
