import os
from typing import List

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SkillMatch"
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    CORS_ORIGINS: List[str] = ["*"]
    ALLOWED_HOSTS: List[str] = ["*"]
    ENVIRONMENT: str = os.getenv("ENVIRONMENT")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    HTTPONLY: bool = os.getenv("HTTPONLY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")


    class Config:
        env_file = ".env"

# CREATE GLOBAL SETTINGS INSTANCE
settings = Settings()