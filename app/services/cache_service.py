import json
from redis.asyncio import Redis
from app.core.config import settings

class RedisCacheService:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    async def get_cache(self, key: str)-> dict:
        cached_value = await self.redis.get(key)
        return json.loads(cached_value) if cached_value is not None else None

    async def set_cache(self, key: str, value, expiry: int = settings.CACHE_EXPIRY) -> None:
        await self.redis.set(key, json.dumps(value), ex=expiry)

    async def invalidate_cache(self, key: str) -> None:
        await self.redis.delete(key)
