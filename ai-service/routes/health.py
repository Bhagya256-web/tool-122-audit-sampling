import time
from flask import Blueprint, jsonify
from services.groq_client import get_avg_response_time_ms

health_bp = Blueprint("health", __name__)

# Track start time and response times
_start_time = time.time()
_response_times = []


def record_response_time(duration_ms: float):
    """Called by other routes to record their response time."""
    _response_times.append(duration_ms)
    if len(_response_times) > 100:
        _response_times.pop(0)


def get_avg_response_time():
    if not _response_times:
        return None
    return round(sum(_response_times) / len(_response_times), 2)


@health_bp.route("/health", methods=["GET"])
def health():
    uptime_seconds = int(time.time() - _start_time)
    return jsonify({
        "status": "ok",
        "model": "llama-3.3-70b-versatile",
        "uptime_seconds": uptime_seconds,
        "avg_response_time_ms": get_avg_response_time(),
        "groq_avg_response_time_ms": get_avg_response_time_ms(),
        "total_requests_tracked": len(_response_times),
    }), 200