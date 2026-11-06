"""Load plain-text documents from a directory."""
from pathlib import Path

def load_documents(directory: str | Path) -> dict[str, str]:
    """Return {relative_document_name: text}; ignore non-TXT and unreadable files."""
    root = Path(directory)
    root.mkdir(parents=True, exist_ok=True)
    documents = {}
    for path in sorted(root.rglob("*.txt")):
        if not path.is_file():
            continue
        try:
            documents[path.relative_to(root).as_posix()] = path.read_text(
                encoding="utf-8-sig", errors="replace"
            )
        except OSError:
            # A single unreadable document should not prevent the remaining corpus loading.
            continue
    return documents
