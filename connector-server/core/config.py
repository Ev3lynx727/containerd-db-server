from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Database
    database_url: str = "mysql://user:password@localhost/db"
    database_password: Optional[str] = None
    
    # Redis
    redis_url: str = "redis://localhost:6380/0"
    
    # Security
    secret_key: str = "change-this-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    api_keys_enabled: bool = True
    
    # API
    api_port: int = 3000
    debug: bool = False
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000"]
    
    # Logging
    log_level: str = "INFO"
    
    # Server mode
    server_mode: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
