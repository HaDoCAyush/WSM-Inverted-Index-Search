"""Wildcard expansion against the index vocabulary."""
import re
from app.modules.normalizer import normalize_token

def wildcard_to_regex(pattern: str) -> re.Pattern:
    """Translate * (zero or more chars) and ? (one char) into a safe regex."""
    normalized = normalize_token(pattern)
    expression = "".join(".*" if char == "*" else "." if char == "?" else re.escape(char)
                         for char in normalized)
    return re.compile(rf"^{expression}$")

def expand_wildcard(pattern: str, vocabulary: set[str], limit: int = 100) -> list[str]:
    """Return alphabetically sorted matching terms, capped to avoid huge expansions."""
    if not any(char in pattern for char in "*?"):
        return [normalize_token(pattern)]
    regex = wildcard_to_regex(pattern)
    return sorted(term for term in vocabulary if regex.fullmatch(term))[:limit]
