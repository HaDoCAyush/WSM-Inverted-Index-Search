"""Production WSGI entry point (Gunicorn: gunicorn wsgi:app)."""
from app import create_app

app = create_app()
