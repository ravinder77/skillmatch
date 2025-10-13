import os
from typing import List
from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SkillMatch"
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    CORS_ORIGINS: List[str] = ["*"]
    ALLOWED_HOSTS: List[str] = ["*"]
    ENVIRONMENT: str = "development"
    ALGORITHM: str = "HS256"
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SECRET_KEY: str
    OPENAI_API_KEY: str

    AWS_S3_BUCKET: str | None = None
    AWS_DEFAULT_REGION: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class TestingSettings(Settings):
    """Overrides with safe defaults for pytest runs."""
    ENVIRONMENT: str = "test"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SECRET_KEY: str = "test-secret-key"
    DATABASE_URL: str = "sqlite:///./test.db"


class ProductionSettings(Settings):
    ENVIRONMENT: str = "production"
    DEBUG: bool = False


# --- Factory for choosing the right settings ---
@lru_cache
def get_settings() -> Settings:
    env = os.getenv("ENVIRONMENT", "development").lower()
    if env == "test" or os.getenv("PYTEST_CURRENT_TEST"):
        return TestingSettings()
    elif env == "production":
        return ProductionSettings()
    return Settings()



try:
    settings = get_settings()
except ValidationError as e:
    raise RuntimeError("Missing critical environment variables. Please check your .env file.") from e



