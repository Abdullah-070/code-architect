from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from routes import gemini_routes, analysis_routes

load_dotenv()

app = Flask(__name__)

# CORS configuration
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
CORS(app, resources={r"/api/*": {"origins": origins}})

# Health check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "Code Architect API"})

# Register blueprints
app.register_blueprint(gemini_routes.bp, url_prefix="/api/gemini")
app.register_blueprint(analysis_routes.bp, url_prefix="/api/analysis")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
