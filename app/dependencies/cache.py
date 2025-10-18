# app/dependencies/cache.py
from fastapi import Depends
from app.dependencies.redis import get_redis
from app.services.cache_service import RedisCacheService
from redis.asyncio import Redis

async def get_cache_service(redis: Redis = Depends(get_redis)) -> RedisCacheService:
    return RedisCacheService(redis)
