import hashlib
import json
import logging
import os
import redis

logger = logging.getLogger(__name__)

CACHE_TTL = 900  # 15 minutes in seconds

_redis_client = None


def get_redis():
    """Get Redis client — returns None if Redis is unavailable."""
    global _redis_client
    if _redis_client is None:
        try:
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
            if redis_url == "memory://":
                return None
            _redis_client = redis.from_url(redis_url, decode_responses=True)
            _redis_client.ping()
        except Exception as e:
            logger.warning(f"Redis unavailable: {e}. Running without cache.")
            _redis_client = None
    return _redis_client


def make_cache_key(endpoint: str, data: dict) -> str:
    """Generate SHA256 cache key from endpoint and input data."""
    raw = f"{endpoint}:{json.dumps(data, sort_keys=True)}"
    return hashlib.sha256(raw.encode()).hexdigest()


def get_cached(endpoint: str, data: dict):
    """Get cached response — returns None if not found or Redis unavailable."""
    try:
        r = get_redis()
        if r is None:
            return None
        key = make_cache_key(endpoint, data)
        cached = r.get(key)
        if cached:
            logger.info(f"Cache HIT for {endpoint}")
            return json.loads(cached)
        logger.info(f"Cache MISS for {endpoint}")
        return None
    except Exception as e:
        logger.warning(f"Cache get failed: {e}")
        return None


def set_cached(endpoint: str, data: dict, result: dict):
    """Store response in cache with 15 min TTL."""
    try:
        r = get_redis()
        if r is None:
            return
        key = make_cache_key(endpoint, data)
        r.setex(key, CACHE_TTL, json.dumps(result))
        logger.info(f"Cache SET for {endpoint} with TTL {CACHE_TTL}s")
    except Exception as e:
        logger.warning(f"Cache set failed: {e}")