from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#Dependency for fastapi routes

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

