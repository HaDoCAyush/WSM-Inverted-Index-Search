"""Parse and execute a deliberately small Boolean query language."""
import re
from app.modules.normalizer import normalize_text
from app.modules.tokenizer import tokenize
from app.modules.wildcard_processor import expand_wildcard

class QueryProcessor:
    """Supports implicit/explicit AND, OR groups, and * / ? term wildcards."""

    def __init__(self, index):
        self.index = index

    def _parse(self, query: str) -> tuple[list[str], str]:
        normalized = normalize_text(query)
        # Split on whitespace; Boolean operators are reserved standalone words.
        raw_parts = normalized.split()
        if not raw_parts:
            raise ValueError("Please enter at least one searchable term.")
        operators = [part.upper() for part in raw_parts if part.upper() in {"AND", "OR"}]
        if "AND" in operators and "OR" in operators:
            raise ValueError("Do not mix AND and OR in one query. Use one operator at a time.")
        operator = "OR" if "OR" in operators else "AND"
        terms = [part for part in raw_parts if part.upper() not in {"AND", "OR"}]
        if not terms:
            raise ValueError("Your query must contain a search term.")
        if any(not re.search(r"[\w*?]", term, re.UNICODE) for term in terms):
            raise ValueError("Each query term must contain letters, numbers, or wildcard characters.")
        return terms, operator

    def search(self, query: str) -> list[dict]:
        terms, operator = self._parse(query)
        expanded = []
        for term in terms:
            matches = expand_wildcard(term, self.index.vocabulary)
            if not matches:
                expanded.append([])
            else:
                expanded.append(matches)

        term_document_sets = []
        for alternatives in expanded:
            docs = set()
            for term in alternatives:
                docs |= self.index.documents_for(term)
            term_document_sets.append(docs)

        if operator == "AND":
            matched_docs = set.intersection(*term_document_sets) if term_document_sets else set()
        else:
            matched_docs = set.union(*term_document_sets) if term_document_sets else set()

        results = []
        for doc_id in matched_docs:
            score = 0
            matched_terms = []
            for alternatives in expanded:
                for term in alternatives:
                    frequency = self.index.term_frequency(term, doc_id)
                    if frequency:
                        score += frequency
                        matched_terms.append(term)
            preview = self._make_preview(self.index.documents[doc_id], matched_terms)
            results.append({
                "document": doc_id,
                "score": score,
                "matched_terms": sorted(set(matched_terms)),
                "preview": preview,
            })
        results.sort(key=lambda item: (-item["score"], item["document"].casefold()))
        return results

    @staticmethod
    def _make_preview(text: str, matched_terms: list[str], limit: int = 240) -> str:
        clean = " ".join(text.split())
        if len(clean) <= limit:
            return clean
        # Keep the beginning as a stable, safe preview; full documents are not exposed.
        return clean[:limit].rstrip() + "…"
