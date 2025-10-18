from fastapi import Request
from app.core.redis_client import RedisClient

async def get_redis():
    """Get Redis client """
    return await RedisClient.get_client()