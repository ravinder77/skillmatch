
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    #CORE
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    # Network & CORS
    CORS_ORIGINS: List[str] = ["*"]
    ALLOWED_HOSTS: List[str] = ["*"]
    #DATABASE
    DATABASE_URL: str
    # Authentication & Security
    ALGORITHM: str = "HS256"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRY: int = 30
    REFRESH_TOKEN_EXPIRY: int = 1440

    SECRET_KEY: str
    REDIS_URL: str
    CACHE_EXPIRY: int = 300

    # Optional AWS
    AWS_S3_BUCKET: Optional[str] = None
    AWS_DEFAULT_REGION: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()

