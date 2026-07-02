"""SkyBook - Airline Ticket Reservation System.

Flask application factory.
"""

from flask import Flask


def create_app() -> Flask:
    """Create and configure the Flask application instance."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev"  # replace with env var before production

    @app.get("/")
    def index() -> str:
        return "SkyBook is running."

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app
