import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SkillMatch"
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    CORS_ORIGINS: List[str] = ["*"]
    ALLOWED_HOSTS: List[str] = ["*"]
    ENVIRONMENT: str = "development"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    SECRET_KEY: str
    DATABASE_URL: str
    AWS_S3_BUCKET: str
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 587
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str


    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")




class TestingSettings(Settings):
    """Overrides with safe defaults for pytest runs."""
    ENVIRONMENT: str = "test"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SECRET_KEY: str = "test-secret-key"
    DATABASE_URL: str = "sqlite:///./test.db"
    AWS_S3_BUCKET: str = "test-bucket"



# --- Factory for choosing the right settings ---
def get_settings() -> Settings:
    env = os.getenv("ENVIRONMENT", "development")
    if env == "test" or "PYTEST_CURRENT_TEST" in os.environ:
        return TestingSettings()

    return Settings()


settings = get_settings()


