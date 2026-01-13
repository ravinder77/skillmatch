from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # CORE
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = 'skillmatch'
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # Network & CORS
    CORS_ORIGINS: List[str] = ["*"]
    ALLOWED_HOSTS: List[str] = ["*"]

    # DATABASE
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # Authentication & Security
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_SECRET: str
    REFRESH_TOKEN_SECRET: str
    ACCESS_TOKEN_EXPIRY: int = 30
    REFRESH_TOKEN_EXPIRY: int = 1440

    # Optional AWS
    AWS_S3_BUCKET: Optional[str] = None
    AWS_DEFAULT_REGION: Optional[str] = None

    # MAIL SETTINGS
    MAILTRAP_HOST: str
    MAILTRAP_PORT: int
    MAILTRAP_USER: str
    MAILTRAP_PASS: str
    SENDER_EMAIL: str

    # RABBITMQ URL
    RABBITMQ_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
