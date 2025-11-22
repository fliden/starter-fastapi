"""Application configuration using pydantic-settings."""

from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application settings
    app_name: str = Field(default="starter-fastapi", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    app_description: str = Field(
        default="Production-ready FastAPI starter template",
        description="Application description",
    )
    environment: str = Field(
        default="development", description="Environment (development, staging, production)"
    )

    # Server settings
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port", ge=1, le=65535)
    reload: bool = Field(default=False, description="Enable auto-reload (development only)")

    # CORS settings
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins",
    )
    cors_credentials: bool = Field(default=True, description="Allow credentials in CORS")
    cors_methods: list[str] = Field(default=["*"], description="Allowed HTTP methods")
    cors_headers: list[str] = Field(default=["*"], description="Allowed HTTP headers")

    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format (json or console)")

    # API settings
    api_v1_prefix: str = Field(default="/api/v1", description="API v1 prefix")

    # Security
    secret_key: str = Field(
        default="your-secret-key-here-change-in-production",
        description="Secret key for signing tokens",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        if isinstance(v, list):
            return v
        return []

    @field_validator("cors_methods", mode="before")
    @classmethod
    def parse_cors_methods(cls, v: Any) -> list[str]:
        """Parse CORS methods from string or list."""
        if isinstance(v, str):
            return [method.strip() for method in v.split(",")]
        if isinstance(v, list):
            return v
        return []

    @field_validator("cors_headers", mode="before")
    @classmethod
    def parse_cors_headers(cls, v: Any) -> list[str]:
        """Parse CORS headers from string or list."""
        if isinstance(v, str):
            return [header.strip() for header in v.split(",")]
        if isinstance(v, list):
            return v
        return []

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value."""
        allowed_environments = {"development", "staging", "production"}
        if v.lower() not in allowed_environments:
            raise ValueError(f"Environment must be one of {allowed_environments}")
        return v.lower()

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"

    @property
    def is_staging(self) -> bool:
        """Check if running in staging environment."""
        return self.environment == "staging"


# Global settings instance
settings = Settings()
