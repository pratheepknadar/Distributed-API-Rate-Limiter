from flask import Flask, jsonify
from rate_limiter import FixedWindowRateLimiter, rate_limit
import redis

# ------------------------------
# Initialize Redis (localhost)
# ------------------------------
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
    socket_timeout=2,
)

# ------------------------------
# Rate limiter configuration
# Example: 5 requests per 10 seconds
# ------------------------------
limiter = FixedWindowRateLimiter(
    redis_client=redis_client,
    window_size=10,      # seconds
    max_requests=5       # requests per window
)

# ------------------------------
# Flask app setup
# ------------------------------
app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"message": "Welcome! Try GET /data"})


@app.route("/data")
@rate_limit(limiter)
def data():
    return jsonify({"message": "You accessed protected data!"})


@app.route("/ping")
def ping():
    return jsonify({"status": "ok"})


# ------------------------------
# Entry point
# ------------------------------
if __name__ == "__main__":
    print("🔥 Flask API running with Redis rate limiting...")
    app.run(host="0.0.0.0", port=5000, debug=True)
