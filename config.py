import os
from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/smartsecurec3"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # JWT
    jwt_secret_key: str = "your-secret-key-here"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    
    # AI Services
    ai_detection_threshold: float = 0.7
    max_concurrent_streams: int = 10
    
    # File Storage
    upload_folder: str = "./uploads"
    max_upload_size: int = 10485760  # 10MB
    
    # Email (for notifications)
    smtp_host: str = "localhost"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = "noreply@smartsecurec3.com"
    
    # API Configuration
    api_v1_prefix: str = "/api/v1"
    debug: bool = False
    
    # Security
    allowed_hosts: list = ["localhost", "127.0.0.1", "*.smartsecurec3.com"]
    cors_origins: list = ["http://localhost:5173", "http://localhost:3000"]
    
    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()