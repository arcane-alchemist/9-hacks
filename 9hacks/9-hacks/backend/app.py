from flask import Flask, jsonify

# Import blueprints from the routes package
from routes.deadline import deadline_bp
from routes.keywords import keywords_bp
from routes.letter_generator import letter_bp


def create_app() -> Flask:
    """
    Application factory for the JusticeAI backend.

    Creates the Flask app instance, registers blueprints,
    and returns the configured app.
    """
    app = Flask(__name__)

    # Register feature-specific blueprints
    app.register_blueprint(deadline_bp)
    app.register_blueprint(keywords_bp)
    app.register_blueprint(letter_bp)

    @app.route("/health", methods=["GET"])
    def health_check():
        """
        Simple health check endpoint to verify that the backend is running.
        """
        return jsonify({"status": "ok", "service": "JusticeAI backend"})

    return app


if __name__ == "__main__":
    # Run the Flask development server on port 5000
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

