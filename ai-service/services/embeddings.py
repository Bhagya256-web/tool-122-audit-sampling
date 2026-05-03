import logging
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

_model = None


def load_model():
    """
    Pre-load sentence-transformers model at startup.
    This avoids delay on first request.
    """
    global _model
    try:
        logger.info("Loading sentence-transformers model...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("sentence-transformers model loaded successfully!")
    except Exception as e:
        logger.error(f"Failed to load sentence-transformers model: {e}")
        _model = None


def get_model():
    """Get the loaded model — returns None if not loaded."""
    return _model


def get_embedding(text: str):
    """
    Get embedding for a text string.
    Returns None if model not loaded.
    """
    if _model is None:
        logger.warning("Model not loaded — returning None")
        return None
    try:
        embedding = _model.encode(text)
        return embedding.tolist()
    except Exception as e:
        logger.error(f"Failed to get embedding: {e}")
        return None