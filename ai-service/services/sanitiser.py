import re
import html

# Patterns that indicate a prompt injection attempt
INJECTION_PATTERNS = [
    r"ignore (all |previous |above )?instructions",
    r"you are now",
    r"disregard (all |your |previous )?",
    r"jailbreak",
    r"system prompt",
    r"forget (everything|your instructions)",
]

# Basic SQL injection patterns
SQL_PATTERNS = [
    r"(--|;|\/\*|\*\/)",
    r"\b(DROP|ALTER|TRUNCATE|INSERT|UPDATE|DELETE|EXEC|UNION|SELECT)\b",
]


def sanitise_input(text: str) -> tuple:
    """
    Sanitise a user input string.
    Returns (cleaned_text, is_suspicious).
    is_suspicious=True means the caller should return HTTP 400.
    """
    if not isinstance(text, str):
        return "", True

    text = text.strip()

    if not text:
        return "", True

    text = html.escape(text)

    lower = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, lower):
            return text, True

    for pattern in SQL_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return text, True

    return text, False