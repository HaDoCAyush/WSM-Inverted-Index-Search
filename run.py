"""Local development entry point."""
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Debug is deliberately disabled by default.
    app.run(host="127.0.0.1", port=5000, debug=False)
