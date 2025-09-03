from app.db.session import engine
from sqlalchemy.orm import Session
from app.db.base import Base
from app import models

def init_db() -> None:
    # This will create all tables if they don’t exist
    Base.metadata.create_all(bind=engine)