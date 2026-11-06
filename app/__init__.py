"""Flask application factory."""
from pathlib import Path
from flask import Flask
from app.modules.document_loader import load_documents
from app.modules.inverted_index import InvertedIndex
from app.routes import create_blueprint

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY="wsm-classroom-project-change-before-public-production",
        DOCUMENT_DIR=PROJECT_ROOT / "data" / "documents",
        MAX_CONTENT_LENGTH=1024 * 1024,
    )
    if test_config:
        app.config.update(test_config)

    documents = load_documents(app.config["DOCUMENT_DIR"])
    index = InvertedIndex()
    index.build(documents)
    app.extensions["search_index"] = index
    app.extensions["documents"] = documents
    app.register_blueprint(create_blueprint())
    return app
