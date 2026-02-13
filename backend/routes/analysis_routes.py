from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import json

bp = Blueprint("analysis", __name__)

@bp.route("/upload-repo", methods=["POST"])
def upload_repository():
    """
    Upload repository files for analysis
    """
    try:
        uploaded_files = []
        if "files" not in request.files:
            return jsonify({"error": "No files provided"}), 400
        
        files = request.files.getlist("files")
        for file in files:
            if file:
                filename = secure_filename(file.filename)
                content = file.read()
                uploaded_files.append({
                    "filename": filename,
                    "size": len(content),
                    "content_type": file.content_type
                })
        
        return jsonify({"uploaded": uploaded_files, "count": len(uploaded_files)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/health", methods=["GET"])
def health():
    """Health check for analysis routes"""
    return jsonify({"status": "healthy", "service": "analysis-routes"})
