"""Application configuration using pydantic-settings."""

from typing import Literal

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

    # Application
    APP_NAME: str = Field(default="AI Code Generation API", description="Application name")
    APP_VERSION: str = Field(default="0.1.0", description="Application version")
    ENVIRONMENT: Literal["development", "staging", "production"] = Field(
        default="development", description="Deployment environment"
    )
    DEBUG: bool = Field(default=False, description="Enable debug mode")

    # Security
    SECRET_KEY: str = Field(
        ..., description="Secret key for signing tokens (generate with: openssl rand -hex 32)"
    )

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/aicodegen",
        description="PostgreSQL async connection URL",
    )

    # Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0", description="Redis connection URL"
    )

    # JWT Configuration
    JWT_SECRET_KEY: str = Field(..., description="JWT signing secret key")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30, description="Access token expiration in minutes"
    )
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7, description="Refresh token expiration in days"
    )

    # Email Configuration
    SENDGRID_API_KEY: str = Field(default="", description="SendGrid API key for email service")
    EMAIL_FROM: str = Field(
        default="noreply@aicodegen.example.com", description="Default sender email"
    )

    # Frontend Configuration
    FRONTEND_URL: str = Field(
        default="http://localhost:3000", description="Frontend application URL for CORS"
    )

    # Email Verification
    VERIFICATION_TOKEN_EXPIRE_HOURS: int = Field(
        default=24, description="Email verification token expiration in hours"
    )

    @field_validator("SECRET_KEY", "JWT_SECRET_KEY")
    @classmethod
    def validate_secret_keys(cls, v: str) -> str:
        """Validate that secret keys are provided and have sufficient length."""
        if not v or len(v) < 32:
            raise ValueError("Secret keys must be at least 32 characters long")
        return v

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL format."""
        if not v.startswith(("postgresql://", "postgresql+asyncpg://")):
            raise ValueError("DATABASE_URL must be a PostgreSQL connection string")
        return v

    @field_validator("REDIS_URL")
    @classmethod
    def validate_redis_url(cls, v: str) -> str:
        """Validate Redis URL format."""
        if not v.startswith("redis://"):
            raise ValueError("REDIS_URL must start with redis://")
        return v

    @field_validator("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    @classmethod
    def validate_access_token_expire(cls, v: int) -> int:
        """Validate access token expiration is reasonable."""
        if v < 5 or v > 1440:  # Between 5 minutes and 24 hours
            raise ValueError("JWT_ACCESS_TOKEN_EXPIRE_MINUTES must be between 5 and 1440")
        return v

    @field_validator("JWT_REFRESH_TOKEN_EXPIRE_DAYS")
    @classmethod
    def validate_refresh_token_expire(cls, v: int) -> int:
        """Validate refresh token expiration is reasonable."""
        if v < 1 or v > 90:  # Between 1 and 90 days
            raise ValueError("JWT_REFRESH_TOKEN_EXPIRE_DAYS must be between 1 and 90")
        return v


# Global settings instance
settings = Settings()
