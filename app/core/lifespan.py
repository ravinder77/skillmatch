from contextlib import asynccontextmanager
from app.db.init_db import init_db
from app.core.redis_client import RedisClient
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

        # Initialize Redis
        redis_client =  await RedisClient.get_client()
        logger.info("✅ Redis database initialized successfully.")

        # Store in app state
        app.state.redis = redis_client
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise e
    yield
    logger.info("👋 Shutting down SkillMatch application...")

    try:
        if redis_client:
          await RedisClient.close()
          logger.info("Redis disconnected")
    except Exception as e:
        logger.error(f"❌ Redis shutdown error: {e}", exc_info=True)
        raise e
