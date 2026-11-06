"""Text normalization and case folding."""
import unicodedata

def normalize_text(text: str) -> str:
    """Normalize Unicode and apply case folding for case-insensitive matching."""
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("’", "'").replace("‘", "'")
    return text.casefold()

def normalize_token(token: str) -> str:
    return normalize_text(token).strip()
