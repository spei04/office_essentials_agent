"""
Configuration management for the API.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = False
    
    # Database
    database_url: str = "sqlite:///./data/app.db"
    
    # AWS
    aws_region: str = "us-east-1"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    
    # Vendor API Keys
    amazon_access_key: str = ""
    amazon_secret_key: str = ""
    amazon_associate_tag: str = ""
    
    staples_api_key: str = ""
    staples_api_secret: str = ""
    
    costco_api_key: str = ""
    costco_api_secret: str = ""
    
    # Policy Settings
    default_budget_limit: float = 1000.00
    require_approval_above: float = 500.00
    
    # Preferences
    preferred_vendors: str = "amazon,staples"
    preferred_brands: str = ""
    
    # CORS
    cors_origins: str = "http://localhost:8000"
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Logging
    log_level: str = "INFO"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def preferred_vendors_list(self) -> List[str]:
        """Get preferred vendors as a list."""
        return [v.strip() for v in self.preferred_vendors.split(",") if v.strip()]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

