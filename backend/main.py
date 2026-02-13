from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()


def create_app():
    """Application factory for Flask."""
    app = Flask(__name__)

    # CORS — allow frontend origins on all /api/* routes
    origins = os.getenv(
        "ALLOWED_ORIGINS", "http://localhost:3000"
    ).split(",")
    CORS(app, resources={r"/*": {"origins": [o.strip() for o in origins]}})

    # ── Health check ────────────────────────────────────────────
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "healthy", "service": "Code Architect API"})

    # ── Register blueprints ─────────────────────────────────────
    from routes.gemini_routes import bp as gemini_bp
    from routes.analysis_routes import bp as analysis_bp

    app.register_blueprint(gemini_bp, url_prefix="/api/gemini")
    app.register_blueprint(analysis_bp, url_prefix="/api/analysis")

    return app


# Gunicorn needs `app` at module level
app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
