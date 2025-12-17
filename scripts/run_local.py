#!/usr/bin/env python3
"""
Local development runner.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.main import app
from api.config import settings
import uvicorn


if __name__ == "__main__":
    print(f"Starting API server on {settings.api_host}:{settings.api_port}")
    print(f"API docs available at http://{settings.api_host}:{settings.api_port}/docs")
    
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_debug,
    )

