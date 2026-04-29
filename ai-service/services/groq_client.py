import os
import time
import logging
from groq import Groq

logger = logging.getLogger(__name__)

_client = None

def get_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set in environment variables")
        _client = Groq(api_key=api_key)
    return _client


def call_groq(messages: list, temperature: float = 0.3, max_tokens: int = 1000) -> str:
    """
    Call Groq API with 3-retry exponential backoff.
    Returns response text, or raises exception after all retries fail.
    """
    client = get_client()
    last_error = None

    for attempt in range(1, 4):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content

        except Exception as e:
            last_error = e
            wait = 2 ** attempt
            logger.error(f"Groq call failed (attempt {attempt}/3): {e}. Retrying in {wait}s...")
            time.sleep(wait)

    raise RuntimeError(f"Groq API failed after 3 attempts: {last_error}")