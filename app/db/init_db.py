from app.db.session import engine
from sqlalchemy.orm import Session
from app.db.base import Base
from app import models

async def init_db() -> None:
    """Create all database tables asynchronously."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)