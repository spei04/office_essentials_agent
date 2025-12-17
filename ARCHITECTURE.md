# Office Essentials Procurement Agent - Architecture & Code Structure

## System Architecture (Small-Scale Design)

```
┌─────────────────┐
│   Web Frontend  │  (Static HTML/JS - Served via S3)
│  (Customer UI)  │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│  FastAPI Backend│  (Single EC2 instance)
│  (REST API)     │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│   RDS  │ │ Procurement │
│ (PostgreSQL)│ │    Agent     │
│  (db.t3.micro)│ │  (Same Process)│
└────────┘ └──────────────┘
                │
                ▼
         ┌─────────────┐
         │  Vendors     │
         │ (Amazon, etc)│
         └─────────────┘
```

## Design Decisions for Small Scale

1. **Single EC2 Instance**: One instance runs both API and agent (no container orchestration)
2. **Simple Database**: Single RDS instance (db.t3.micro) or SQLite for very small scale
3. **Static Frontend**: Simple HTML/JS (or lightweight React) hosted on S3
4. **No Load Balancer**: Direct EC2 access or simple API Gateway
5. **In-Process Background Jobs**: Python asyncio/threading instead of Celery/RQ
6. **Minimal AWS Services**: EC2, RDS, S3, CloudFront (optional)

## Complete Code Structure

```
office_essentials_agent/
│
├── README.md
├── ARCHITECTURE.md              # This file
├── pyproject.toml
├── requirements.txt
├── .env.example
├── .gitignore
│
├── frontend/                    # Simple Web Application
│   ├── index.html               # Main HTML page
│   ├── css/
│   │   └── style.css            # Simple CSS styling
│   ├── js/
│   │   ├── app.js               # Main application logic
│   │   ├── api.js               # API client
│   │   └── utils.js             # Utility functions
│   └── assets/                  # Images, icons
│
├── api/                         # FastAPI Backend (Single Process)
│   ├── __init__.py
│   ├── main.py                  # FastAPI app + agent integration
│   ├── config.py                 # Configuration management
│   │
│   ├── routes/                   # API endpoints
│   │   ├── __init__.py
│   │   ├── customers.py         # Customer endpoints
│   │   ├── procurement.py       # Procurement request endpoints
│   │   ├── orders.py            # Order status endpoints
│   │   └── health.py            # Health check
│   │
│   ├── models/                   # SQLAlchemy database models
│   │   ├── __init__.py
│   │   ├── base.py              # Base model
│   │   ├── customer.py          # Customer model
│   │   ├── order.py             # Order model
│   │   └── order_item.py        # Order item model
│   │
│   ├── schemas/                  # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── customer.py
│   │   ├── procurement.py
│   │   └── order.py
│   │
│   ├── services/                 # Business logic
│   │   ├── __init__.py
│   │   ├── customer_service.py
│   │   ├── procurement_service.py  # Orchestrates agent
│   │   └── order_service.py
│   │
│   └── database/
│       ├── __init__.py
│       ├── connection.py        # DB connection (SQLite or PostgreSQL)
│       └── migrations/           # Alembic migrations (optional)
│
├── agent/                        # Procurement Agent (Same Process)
│   ├── __init__.py
│   ├── planner.py               # Task planning
│   ├── search.py                 # Product search
│   ├── optimizer.py             # Price optimization
│   ├── purchaser.py             # Purchase execution
│   └── schemas.py                # Agent data models
│
├── integrations/                 # Vendor integrations
│   ├── __init__.py
│   ├── base.py                   # Base vendor interface
│   ├── amazon.py                 # Amazon API
│   ├── staples.py                # Staples API
│   ├── costco.py                 # Costco API
│   └── mock_vendor.py            # Mock vendor for testing
│
├── policies/                     # Business rules
│   ├── __init__.py
│   ├── budget.py                 # Budget constraints
│   ├── preferences.py            # User preferences
│   └── approvals.py              # Approval workflows
│
├── workflows/                    # End-to-end workflows
│   ├── __init__.py
│   └── procure_office_essentials.py
│
├── aws/                          # AWS Deployment (Simplified)
│   ├── cloudformation/
│   │   ├── infrastructure.yaml   # Single stack: EC2 + RDS + S3
│   │   └── security-groups.yaml  # Security groups
│   │
│   ├── ec2/
│   │   ├── user-data.sh          # EC2 initialization script
│   │   └── startup.sh            # Application startup script
│   │
│   └── scripts/
│       ├── deploy.sh              # Simple deployment script
│       └── setup.sh              # Initial AWS setup
│
├── tests/                        # Test suite
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
└── scripts/                      # Utility scripts
    ├── setup_db.py              # Database initialization
    ├── seed_data.py             # Seed test data
    └── run_local.py             # Local development runner
```

## Key Components (Simplified)

### Frontend (Simple HTML/JS)
- **Single Page Application**: One HTML file with embedded JS
- **Vanilla JavaScript**: No framework complexity
- **Simple Styling**: CSS only, no build process
- **Direct API Calls**: Fetch API for REST calls
- **Optional**: Lightweight React if needed for interactivity

### API Backend (FastAPI - Single Process)
- **Monolithic Structure**: API and agent in same process
- **Async Processing**: Python asyncio for background tasks (no Celery)
- **Simple Database**: SQLite for development, PostgreSQL (RDS) for production
- **In-Memory Queue**: Simple queue for processing procurement requests
- **No Authentication**: Simple API keys or basic auth (can add JWT later)

### Procurement Agent
- **Same Process**: Runs in same Python process as API
- **Background Tasks**: asyncio tasks for async processing
- **Simple Queue**: In-memory or SQLite-based queue
- **Synchronous Processing**: Process requests as they come

### AWS Infrastructure (Minimal)
- **EC2**: Single t3.small or t3.medium instance
  - Runs FastAPI with uvicorn
  - Handles all API requests and agent processing
- **RDS**: Single db.t3.micro PostgreSQL instance (or SQLite for very small)
- **S3**: Static frontend hosting
- **Optional CloudFront**: CDN for frontend (can skip initially)
- **Security Group**: Simple rules for HTTP/HTTPS access

## Data Flow (Simplified)

1. **Customer submits request** → Frontend → FastAPI endpoint
2. **API creates order** → Stores in database → Queues async task
3. **Agent processes** (same process) → Searches → Optimizes → Purchases
4. **Agent updates order** → Updates database
5. **Frontend polls** → API returns order status

## Deployment Strategy

### Development
- Run locally: `python -m uvicorn api.main:app --reload`
- SQLite database
- Frontend: Open `frontend/index.html` in browser

### Production (AWS)
1. **EC2 Instance**: 
   - Install Python 3.11+
   - Clone repo
   - Install dependencies: `pip install -r requirements.txt`
   - Run: `uvicorn api.main:app --host 0.0.0.0 --port 8000`
   - Use systemd or supervisor to keep running
2. **RDS**: 
   - Create PostgreSQL instance
   - Update DATABASE_URL in .env
3. **S3**: 
   - Upload frontend/ folder to S3 bucket
   - Enable static website hosting
4. **Optional**: 
   - CloudFront for CDN
   - Route 53 for custom domain

## Cost Estimate (Small Scale)

- **EC2 t3.small**: ~$15/month
- **RDS db.t3.micro**: ~$15/month
- **S3**: ~$1/month (minimal storage)
- **Data Transfer**: ~$5/month
- **Total**: ~$35-40/month

## Scaling Path (If Needed Later)

1. **Add Load Balancer**: If traffic increases
2. **Separate Agent**: Move agent to separate process/instance
3. **Add Caching**: Redis for session/cache
4. **Database Scaling**: RDS read replicas
5. **Frontend Framework**: Move to React if UI complexity grows
