# Office Essentials Procurement Agent

An automated office essentials procurement system that automates product search, price optimization, and purchasing. Built with FastAPI backend and a simple web frontend, designed for small-scale deployments on AWS.

## Features

- **Automated Product Search**: Searches across multiple vendors (Amazon, Staples, Costco)
- **Price Optimization**: Automatically finds the best prices and products
- **Budget Management**: Enforces budget limits and tracks spending
- **Customer Management**: Simple customer registration and order tracking
- **Web Interface**: Clean, simple web UI for customers to submit requests
- **AWS Deployment**: Ready for deployment on EC2 with RDS

## Architecture

- **Frontend**: Simple HTML/JavaScript (no build process)
- **Backend**: FastAPI REST API
- **Agent**: Procurement agent runs in the same process as API
- **Database**: PostgreSQL (RDS) or SQLite (development)
- **Deployment**: Single EC2 instance (no containers)

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

## Quick Start

### Prerequisites

- Python 3.10 or higher
- PostgreSQL (for production) or SQLite (for development)
- AWS account (for deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd office_essentials_agent
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   python scripts/setup_db.py
   ```

6. **Run the API server**
   ```bash
   python scripts/run_local.py
   ```

   The API will be available at `http://localhost:8000`
   - API docs: `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/api/v1/health/`

7. **Open the frontend**
   - Open `frontend/index.html` in your browser
   - Or serve it with a simple HTTP server:
     ```bash
     cd frontend
     python -m http.server 3000
     ```
   - Update `API_BASE_URL` in `frontend/js/api.js` if needed

### Seed Sample Data (Optional)

```bash
python scripts/seed_data.py
```

## Project Structure

```
office_essentials_agent/
├── api/                    # FastAPI backend
│   ├── main.py            # FastAPI app
│   ├── routes/            # API endpoints
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   └── database/          # Database configuration
├── agent/                 # Procurement agent
│   ├── planner.py        # Task planning
│   ├── search.py         # Product search
│   ├── optimizer.py      # Price optimization
│   └── purchaser.py      # Purchase execution
├── integrations/          # Vendor integrations
│   ├── base.py          # Base vendor interface
│   ├── mock_vendor.py   # Mock vendor (for testing)
│   ├── amazon.py        # Amazon API
│   ├── staples.py       # Staples API
│   └── costco.py        # Costco API
├── policies/             # Business rules
│   ├── budget.py        # Budget constraints
│   ├── preferences.py   # User preferences
│   └── approvals.py     # Approval workflows
├── workflows/            # End-to-end workflows
├── frontend/             # Web interface
│   ├── index.html       # Main page
│   ├── css/             # Styles
│   └── js/              # JavaScript
├── aws/                  # AWS deployment
│   ├── ec2/             # EC2 configuration
│   └── scripts/         # Deployment scripts
├── scripts/              # Utility scripts
└── tests/                # Test suite
```

## API Endpoints

### Customers
- `POST /api/v1/customers/` - Create customer
- `GET /api/v1/customers/` - List customers
- `GET /api/v1/customers/{id}` - Get customer
- `PUT /api/v1/customers/{id}` - Update customer
- `DELETE /api/v1/customers/{id}` - Delete customer

### Procurement
- `POST /api/v1/procurement/` - Create procurement request

### Orders
- `GET /api/v1/orders/` - List orders
- `GET /api/v1/orders/{id}` - Get order
- `PATCH /api/v1/orders/{id}/status` - Update order status

### Health
- `GET /api/v1/health/` - Health check

See API documentation at `/docs` when the server is running.

## AWS Deployment

### Prerequisites
- AWS account
- EC2 instance (t3.small recommended)
- RDS PostgreSQL instance (db.t3.micro)
- S3 bucket for frontend

### Deployment Steps

1. **Set up EC2 instance**
   - Launch EC2 instance (Amazon Linux 2)
   - Configure security group (allow HTTP/HTTPS)
   - Use the user-data script in `aws/ec2/user-data.sh`

2. **Set up RDS**
   - Create PostgreSQL database instance
   - Note the connection string
   - Update `DATABASE_URL` in `.env`

3. **Deploy application**
   ```bash
   # Copy files to EC2
   aws/scripts/deploy.sh
   ```

4. **Deploy frontend to S3**
   ```bash
   aws s3 sync frontend/ s3://your-bucket-name/
   aws s3 website s3://your-bucket-name/ --index-document index.html
   ```

5. **Configure API URL**
   - Update `API_BASE_URL` in `frontend/js/api.js` to point to your EC2 instance

### Cost Estimate
- EC2 t3.small: ~$15/month
- RDS db.t3.micro: ~$15/month
- S3: ~$1/month
- **Total: ~$35-40/month**

## Configuration

Key environment variables (see `.env.example`):

- `DATABASE_URL`: Database connection string
- `API_HOST`: API host (default: 0.0.0.0)
- `API_PORT`: API port (default: 8000)
- `DEFAULT_BUDGET_LIMIT`: Default budget limit
- `REQUIRE_APPROVAL_ABOVE`: Approval threshold
- Vendor API keys (Amazon, Staples, Costco)

## Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=api --cov=agent
```

## Development

### Adding a New Vendor

1. Create a new file in `integrations/` (e.g., `new_vendor.py`)
2. Implement the `VendorInterface` from `integrations/base.py`
3. Add vendor to `integrations/__init__.py`
4. Register vendor in `api/services/procurement_service.py`

### Adding New Features

- API endpoints: Add to `api/routes/`
- Business logic: Add to `api/services/`
- Agent logic: Add to `agent/`
- Frontend: Update `frontend/`

## License

MIT License

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

## Support

For issues and questions, please open an issue on GitHub.
