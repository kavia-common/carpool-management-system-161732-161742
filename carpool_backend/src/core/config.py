from functools import lru_cache
from typing import List
from pydantic import BaseModel, Field
import os


class Settings(BaseModel):
    """Application configuration settings sourced from environment variables.

    Important:
    - SECRET_KEY: used for password hashing and token signing in MVP. Provide a strong value in production.
    """
    app_name: str = Field(default="Carpool Backend API", description="Application name")
    environment: str = Field(default=os.getenv("ENV", "development"), description="Environment name")
    cors_origins: List[str] = Field(
        default_factory=lambda: os.getenv("CORS_ORIGINS", "*").split(","),
        description="Allowed CORS origins"
    )
    secret_key: str = Field(default=os.getenv("SECRET_KEY", "dev-secret-key"), description="Secret key")
    access_token_expire_minutes: int = Field(
        default=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")),
        description="Access token expiry in minutes"
    )


# PUBLIC_INTERFACE
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
