import hashlib
import redis
import json
from datetime import timedelta

# Connect to Redis (will start via Docker)
# redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Temporary: in-memory cache for POC without Redis
_cache = {}

def get_idempotency_key(request_id: str, subscriber_id: str) -> str:
    raw = f"{request_id}:{subscriber_id}"
    return hashlib.sha256(raw.encode()).hexdigest()

def is_duplicate(key: str) -> bool:
    return key in _cache

def store_response(key: str, response_data: dict, ttl_hours: int = 24):
    _cache[key] = response_data

def get_cached_response(key: str) -> dict:
    return _cache.get(key)

def get_idempotency_key(request_id: str, subscriber_id: str) -> str:
    """Generate an idempotency key from request ID and subscriber ID"""
    raw = f"{request_id}:{subscriber_id}"
    return hashlib.sha256(raw.encode()).hexdigest()

def is_duplicate(key: str) -> bool:
    """Check if this request has been processed before"""
    return redis_client.exists(key) == 1

def store_response(key: str, response_data: dict, ttl_hours: int = 24):
    """Store the response for idempotency"""
    redis_client.setex(
        key,
        timedelta(hours=ttl_hours),
        json.dumps(response_data)
    )

def get_cached_response(key: str) -> dict:
    """Retrieve cached response"""
    data = redis_client.get(key)
    return json.loads(data) if data else None