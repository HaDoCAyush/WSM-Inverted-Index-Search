"""Build and query an in-memory positional inverted index."""
from collections import defaultdict
from app.modules.tokenizer import tokenize

class InvertedIndex:
    """Maps each normalized term to document IDs and token positions."""

    def __init__(self):
        self.postings: dict[str, dict[str, list[int]]] = defaultdict(dict)
        self.documents: dict[str, str] = {}
        self.vocabulary: set[str] = set()
        self.total_term_occurrences = 0

    def build(self, documents: dict[str, str]) -> None:
        self.postings.clear()
        self.documents = dict(documents)
        self.vocabulary.clear()
        self.total_term_occurrences = 0
        for doc_id, text in self.documents.items():
            for position, term in enumerate(tokenize(text)):
                self.postings[term].setdefault(doc_id, []).append(position)
                self.vocabulary.add(term)
                self.total_term_occurrences += 1

    @property
    def vocabulary_size(self) -> int:
        return len(self.vocabulary)

    def documents_for(self, term: str) -> set[str]:
        return set(self.postings.get(term, {}).keys())

    def term_frequency(self, term: str, doc_id: str) -> int:
        return len(self.postings.get(term, {}).get(doc_id, []))

    def positions(self, term: str, doc_id: str) -> list[int]:
        return list(self.postings.get(term, {}).get(doc_id, []))
