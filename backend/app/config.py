# backend/app/config.py

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "CloudShop API"
    app_description: str = "CloudShop E-Commerce API with reporting and analytics"
    app_version: str = "1.0.0"

    # Database URLs
    database_url: str
    reporting_database_url: str

    # Security
    secret_key: str = "CHANGE_ME"
    access_token_expire_minutes: int = 60

    # CORS
    backend_cors_origins: str | None = None  # comma-separated list

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
