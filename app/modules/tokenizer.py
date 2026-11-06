"""Convert text into word tokens."""
import re
from app.modules.normalizer import normalize_token

# Unicode word characters; apostrophes are allowed only within a token.
TOKEN_PATTERN = re.compile(r"[^\W_]+(?:['’][^\W_]+)*", re.UNICODE)

def tokenize(text: str) -> list[str]:
    """Return normalized tokens in source order."""
    return [normalize_token(match.group(0)) for match in TOKEN_PATTERN.finditer(text)]
