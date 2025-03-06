import redis
import redis.asyncio as async_redis

from app.config import settings

redis_client = redis.Redis.from_url(str(settings.REDIS_DSN))
async_pool = async_redis.ConnectionPool.from_url(str(settings.REDIS_DSN))
