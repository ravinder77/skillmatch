import redis.asyncio as redis
from app.config.settings import settings


class RedisClient:
    _client: redis.Redis | None = None

    @classmethod
    def get_client(cls) -> redis.Redis | None:
        if cls._client is None:
            cls._client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        return cls._client

    @classmethod
    async def close(cls):
        if cls._client is not None:
            await cls._client.close()
            cls._client = None

