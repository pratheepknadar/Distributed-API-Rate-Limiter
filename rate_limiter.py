import time
import redis
from functools import wraps
from flask import jsonify, request


class FixedWindowRateLimiter:
    """
    Production-ready fixed window rate limiter using Redis INCR + EXPIRE.
    """

    def __init__(self, redis_client, window_size=60, max_requests=10):
        self.redis = redis_client
        self.window_size = window_size
        self.max_requests = max_requests

    def _key(self, identifier):
        """
        Identifier may be user_id or IP address.
        """
        current_window = int(time.time() // self.window_size)
        return f"rate_limit:{identifier}:{current_window}"

    def allow(self, identifier):
        """
        Returns dict: {allowed, count, limit, window_seconds_left}
        """
        key = self._key(identifier)

        # Atomic operations
        pipe = self.redis.pipeline()
        pipe.incr(key)
        pipe.ttl(key)
        count, ttl = pipe.execute()

        # If first time this key has been seen — set expiry
        if ttl == -1:
            self.redis.expire(key, self.window_size)
            ttl = self.window_size

        allowed = count <= self.max_requests

        return {
            "allowed": allowed,
            "count": count,
            "limit": self.max_requests,
            "window_seconds_left": ttl
        }


def rate_limit(limiter: FixedWindowRateLimiter):
    """
    Flask decorator for rate limiting endpoints.
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):

            # You can use API key, user_id, JWT, etc.
            # Here we rate-limit by the client's IP.
            client_id = request.remote_addr

            result = limiter.allow(client_id)

            if not result["allowed"]:
                response = {
                    "error": "Too Many Requests",
                    "limit": result["limit"],
                    "used": result["count"],
                    "retry_after_seconds": result["window_seconds_left"]
                }
                return jsonify(response), 429

            # Continue normally
            return fn(*args, **kwargs)

        return wrapper
    return decorator
