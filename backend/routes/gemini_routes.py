from flask import Blueprint, request, jsonify
from models.schemas import RepositoryInput, AnalysisStatus
from services.gemini_service import GeminiService
import uuid

bp = Blueprint("gemini", __name__)
gemini_service = GeminiService()


@bp.route("/analyze", methods=["POST"])
def analyze_repository():
    """Start autonomous analysis of a repository using Gemini."""
    try:
        data = request.get_json()
        repo_input = RepositoryInput(**data)
        analysis_id = str(uuid.uuid4())

        result = gemini_service.start_analysis(
            analysis_id=analysis_id,
            repository_url=repo_input.repository_url,
            branch=repo_input.branch,
            focus_areas=repo_input.focus_areas,
            depth=repo_input.depth,
        )

        return jsonify({
            "analysis_id": analysis_id,
            "status": AnalysisStatus.ANALYZING,
            "repository_url": repo_input.repository_url,
            "findings": result.get("findings"),
            "recommendations": result.get("recommendations"),
            "generated_code": result.get("generated_code"),
        })
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@bp.route("/analyze/<analysis_id>", methods=["GET"])
def get_analysis_status(analysis_id):
    """Get status and results of an ongoing analysis."""
    try:
        result = gemini_service.get_analysis_result(analysis_id)
        if not result:
            return jsonify({"error": "Analysis not found"}), 404
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
