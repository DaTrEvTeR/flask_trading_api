import redis

from app.config.settings import settings

redis_client = redis.Redis(host=settings.redis_host, port=settings.redis_port)
