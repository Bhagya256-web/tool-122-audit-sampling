import os
import time
import logging
from groq import Groq

logger = logging.getLogger(__name__)

_client = None

# Performance tracking
_response_times = []


def get_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set in environment variables")
        _client = Groq(api_key=api_key)
    return _client


def get_avg_response_time_ms() -> float:
    """Return average Groq response time in milliseconds."""
    if not _response_times:
        return None
    return round(sum(_response_times) / len(_response_times), 2)


def call_groq(messages: list, temperature: float = 0.3, max_tokens: int = 1000) -> str:
    """
    Call Groq API with 3-retry exponential backoff.
    Tracks response time for performance monitoring.
    Returns response text, or raises exception after all retries fail.
    """
    client = get_client()
    last_error = None

    for attempt in range(1, 4):
        try:
            start = time.time()

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            # Track response time
            duration_ms = (time.time() - start) * 1000
            _response_times.append(duration_ms)
            if len(_response_times) > 100:
                _response_times.pop(0)

            logger.info(f"Groq call succeeded in {duration_ms:.0f}ms")
            return response.choices[0].message.content

        except Exception as e:
            last_error = e
            wait = 2 ** attempt  # 2s, 4s, 8s
            logger.error(f"Groq call failed (attempt {attempt}/3): {e}. Retrying in {wait}s...")
            time.sleep(wait)

    raise RuntimeError(f"Groq API failed after 3 attempts: {last_error}")