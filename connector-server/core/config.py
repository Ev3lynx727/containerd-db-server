"""
Application settings with environment-based configuration.
"""
from functools import lru_cache
from typing import List, Optional

from pydantic import Field, field_validator, ValidationInfo
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with validation."""

    # Server Configuration
    server_mode: str = Field(
        default="development",
        description="Server mode: development, staging, production"
    )
    api_port: int = Field(
        default=3000,
        ge=1,
        le=65535,
        description="API server port"
    )
    debug: bool = Field(
        default=False,
        description="Enable debug mode"
    )

    # Database Configuration
    database_url: str = Field(
        default="mysql://user:password@localhost/db",
        description="Database connection URL"
    )
    database_password: Optional[str] = Field(
        default=None,
        description="Database password (will override password in URL)"
    )

    # Redis Configuration
    redis_url: str = Field(
        default="redis://localhost:6380/0",
        description="Redis connection URL"
    )
    redis_password: Optional[str] = Field(
        default=None,
        description="Redis password"
    )

    # Security Configuration
    secret_key: str = Field(
        default="change-this-secret-key-in-production",
        min_length=32,
        description="Secret key for JWT tokens"
    )
    algorithm: str = Field(
        default="HS256",
        description="JWT algorithm"
    )
    access_token_expire_minutes: int = Field(
        default=30,
        ge=1,
        le=1440,  # 24 hours max
        description="JWT token expiration time in minutes"
    )
    api_keys_enabled: bool = Field(
        default=True,
        description="Enable API key authentication"
    )

    # CORS Configuration
    cors_origins: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000"],
        description="Allowed CORS origins"
    )

    # Logging Configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )

    # Performance Configuration
    max_connections: int = Field(
        default=100,
        ge=1,
        le=1000,
        description="Maximum database connections"
    )
    connection_timeout: int = Field(
        default=30,
        ge=1,
        le=300,
        description="Database connection timeout in seconds"
    )

    # Rate Limiting
    rate_limit_requests: int = Field(
        default=100,
        ge=1,
        le=10000,
        description="Rate limit requests per window"
    )
    rate_limit_window_seconds: int = Field(
        default=60,
        ge=1,
        le=3600,
        description="Rate limit window in seconds"
    )

    class Config:
        """Pydantic settings configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        env_prefix = "CONNECTOR_"

    @field_validator("database_url", mode="after")
    @classmethod
    def validate_database_url(cls, v: str, info: ValidationInfo) -> str:
        """Validate and enhance database URL."""
        if not v.startswith(("mysql://", "mysql+asyncmy://")):
            raise ValueError("Database URL must use MySQL protocol")

        # If password is provided separately, inject it into URL
        if info.data.get("database_password"):
            # Replace password in URL if it exists
            if "@" in v:
                protocol_and_creds = v.split("@")[0]
                host_and_path = "@" + v.split("@")[1]
                user = protocol_and_creds.split("://")[1].split(":")[0]
                v = (
                    f"{protocol_and_creds.split('://')[0]}://{user}:"
                    f"{info.data['database_password']}{host_and_path}"
                )

        return v

    @field_validator("redis_url", mode="after")
    @classmethod
    def validate_redis_url(cls, v: str, info: ValidationInfo) -> str:
        """Validate Redis URL."""
        if not v.startswith("redis://"):
            raise ValueError("Redis URL must use redis:// protocol")
        return v

    @field_validator("server_mode", mode="after")
    @classmethod
    def validate_server_mode(cls, v: str) -> str:
        """Validate server mode."""
        valid_modes = ["development", "staging", "production"]
        if v.lower() not in valid_modes:
            raise ValueError(f"Server mode must be one of: {', '.join(valid_modes)}")
        return v.lower()

    @field_validator("secret_key", mode="after")
    @classmethod
    def validate_secret_key(cls, v: str, info: ValidationInfo) -> str:
        """Validate secret key strength."""
        if info.data.get("server_mode") == "production" and len(v) < 32:
            raise ValueError("Secret key must be at least 32 characters in production")
        return v

    def get_database_url_async(self) -> str:
        """Get async database URL."""
        return self.database_url.replace("mysql://", "mysql+asyncmy://")

    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.server_mode == "production"

    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.server_mode == "development"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
