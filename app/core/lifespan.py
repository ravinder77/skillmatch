from contextlib import asynccontextmanager
from app.db.init_db import init_db
import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app):
    """
    Lifespan handler for FastAPI.
    Handles startup and shutdown tasks like DB initialization, Redis, etc.
    """
    # --- Startup ---
    logger.info("🚀 Starting SkillMatch application...")
    redis_client = None
    try:
        # Initialize Database
        await init_db()
        logger.info("✅ Database initialized successfully.")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise e
    yield
    logger.info("👋 Shutting down SkillMatch application...")
