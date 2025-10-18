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
    ACCESS_TOKEN_EXPIRY: int = 30        # minutes
    REFRESH_TOKEN_EXPIRY: int = 1440     # 1 day
    SECRET_KEY: str
    OPENAI_API_KEY: str
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_EXPIRY: int = 300
    AWS_S3_BUCKET: str | None = None
    AWS_DEFAULT_REGION: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

