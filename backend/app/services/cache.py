import json
import logging
from typing import Optional, Any

logger = logging.getLogger(__name__)


class CacheService:
    def __init__(self, redis_url: str, ttl: int = 300):
        self.redis_url = redis_url
        self.ttl = ttl
        self._client = None
        self._available = False
        self._try_connect()

    def _try_connect(self):
        try:
            import redis
            self._client = redis.from_url(self.redis_url, socket_connect_timeout=2)
            self._client.ping()
            self._available = True
            logger.info("Redis cache connected")
        except Exception as e:
            logger.warning(f"Redis unavailable, running without cache: {e}")
            self._available = False

    def get(self, key: str) -> Optional[Any]:
        if not self._available:
            return None
        try:
            raw = self._client.get(key)
            if raw:
                return json.loads(raw)
        except Exception as e:
            logger.warning(f"Cache get error: {e}")
        return None

    def set(self, key: str, value: Any) -> bool:
        if not self._available:
            return False
        try:
            self._client.setex(key, self.ttl, json.dumps(value))
            return True
        except Exception as e:
            logger.warning(f"Cache set error: {e}")
            return False

    def delete(self, key: str) -> bool:
        if not self._available:
            return False
        try:
            self._client.delete(key)
            return True
        except Exception as e:
            logger.warning(f"Cache delete error: {e}")
            return False

    @property
    def is_available(self) -> bool:
        return self._available
