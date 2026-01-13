from app.db.session import engine
from app.db.base import metadata


async def init_db() -> None:
    """Create all database tables asynchronously."""
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
