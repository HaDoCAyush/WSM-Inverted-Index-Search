"""HTTP routes and JSON API for the search interface."""
from flask import Blueprint, current_app, jsonify, render_template, request
from app.modules.query_processor import QueryProcessor

def create_blueprint():
    bp = Blueprint("main", __name__)

    @bp.get("/")
    def home():
        return render_template("index.html")

    @bp.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @bp.get("/api/stats")
    def stats():
        index = current_app.extensions["search_index"]
        docs = current_app.extensions["documents"]
        return jsonify({
            "document_count": len(docs),
            "vocabulary_size": index.vocabulary_size,
            "indexed_terms": index.total_term_occurrences,
        })

    @bp.get("/api/search")
    def search():
        query = request.args.get("q", "").strip()
        if not query:
            return jsonify({"query": query, "results": [], "message": "Enter a search query."}), 400
        if len(query) > 120:
            return jsonify({"error": "Query must be 120 characters or fewer."}), 400
        processor = QueryProcessor(current_app.extensions["search_index"])
        try:
            results = processor.search(query)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        return jsonify({
            "query": query,
            "results": results,
            "count": len(results),
            "message": "Results found." if results else "No matching documents found."
        })

    return bp
