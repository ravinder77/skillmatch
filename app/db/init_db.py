from app.db.session import engine
from app.db.base import Base


async def init_db() -> None:
    """Create all database tables asynchronously."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
