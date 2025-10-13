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
    try:
        await init_db()
        logger.info("✅ Database initialized successfully.")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise e

    yield  # 👈 The app runs while inside this block

    # --- Shutdown ---
    logger.info("👋 Shutting down SkillMatch application...")
