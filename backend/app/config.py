from typing import Optional

from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database - Railway provides DATABASE_URL
    DATABASE_URL: Optional[str] = None

    # PostgreSQL specific settings (for local development/docker-compose)
    POSTGRES_DB: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_HOST: Optional[str] = None

    # Security - Defaults for development
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Admin user — seeded into the database on startup
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    ADMIN_EMAIL: str

    # Application
    APP_NAME: str = "Portfolio Blog API"
    DEBUG: bool = False
    LOG_SQL_QUERIES: bool = False  # Set to True to see SQL queries in logs
    CORS_ORIGINS: str = (
        "http://localhost:3000,http://localhost:5173,http://localhost:4000,https://webbpulse.com,https://www.webbpulse.com,http://webbpulse.com"
    )

    # Rate Limiting60
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 1000
    RATE_LIMIT_REQUESTS_PER_HOUR: int = 10000
    RATE_LIMIT_REQUESTS_PER_DAY: int = 100000

    @field_validator("CORS_ORIGINS")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse comma-separated CORS origins string into a list"""
        if isinstance(v, str):
            origins = [origin.strip() for origin in v.split(",") if origin.strip()]
            # Always add localhost origins for development
            localhost_origins = [
                "http://localhost:3000",
                "http://localhost:4000",
                "http://localhost:5173",
                "http://127.0.0.1:3000",
                "http://127.0.0.1:4000",
                "http://127.0.0.1:5173",
            ]
            origins.extend(localhost_origins)
            return list(set(origins))  # Remove duplicates
        return v

    model_config = ConfigDict(env_file=".env")

    def get_database_url(self) -> str:
        """Get database URL - prioritize DATABASE_URL (Railway)"""
        if self.DATABASE_URL:
            return self.DATABASE_URL

        # Fall back to individual components for local development
        if all(
            [
                self.POSTGRES_DB,
                self.POSTGRES_USER,
                self.POSTGRES_PASSWORD,
                self.POSTGRES_HOST,
            ]
        ):
            return (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:5432/{self.POSTGRES_DB}"
            )

        raise ValueError(
            "Database configuration error: Either DATABASE_URL must be set (Railway) "
            "or all individual PostgreSQL components must be set (local development)"
        )


# Create settings instance
settings = Settings()
