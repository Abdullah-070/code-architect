import google.generativeai as genai
from config import Config
from typing import Optional, List, Dict
import threading


class GeminiService:
    """Service for interacting with the Gemini API."""

    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model_name = Config.GEMINI_MODEL
        # In-memory cache (use Redis in production)
        self.analysis_cache: Dict[str, dict] = {}

    # ------------------------------------------------------------------ #
    #  Public API                                                         #
    # ------------------------------------------------------------------ #

    def start_analysis(
        self,
        analysis_id: str,
        repository_url: str,
        branch: str = "main",
        focus_areas: Optional[List[str]] = None,
        depth: int = 3,
    ) -> dict:
        """Kick off an autonomous code analysis in a background thread."""
        analysis_state = {
            "analysis_id": analysis_id,
            "status": "analyzing",
            "repository_url": repository_url,
            "findings": {},
            "recommendations": [],
            "generated_code": [],
            "iteration": 0,
            "max_iterations": depth,
        }
        self.analysis_cache[analysis_id] = analysis_state

        # Run the heavy work on a background thread so the request can
        # return immediately (Flask is synchronous).
        thread = threading.Thread(
            target=self._run_analysis,
            args=(analysis_id, repository_url, focus_areas, depth),
            daemon=True,
        )
        thread.start()

        return analysis_state

    def get_analysis_result(self, analysis_id: str) -> Optional[dict]:
        """Return the current state for *analysis_id*."""
        return self.analysis_cache.get(analysis_id)

    # ------------------------------------------------------------------ #
    #  Background worker                                                  #
    # ------------------------------------------------------------------ #

    def _run_analysis(
        self,
        analysis_id: str,
        repository_url: str,
        focus_areas: Optional[List[str]],
        depth: int,
    ):
        """Synchronous analysis loop executed on a background thread."""
        state = self.analysis_cache[analysis_id]

        try:
            for iteration in range(depth):
                state["iteration"] = iteration + 1

                prompt = self._build_prompt(
                    repository_url, focus_areas, iteration + 1, depth
                )
                response = self._call_gemini(prompt)

                state["findings"][f"iteration_{iteration + 1}"] = response
                state["recommendations"].extend(
                    self._extract_recommendations(response)
                )

                # Self-correction pass (skip on the last iteration)
                if iteration < depth - 1:
                    refinement_prompt = (
                        "Based on the previous analysis, please provide:\n"
                        "1. What we might have missed\n"
                        "2. Deeper architectural insights\n"
                        "3. Cross-cutting concerns\n"
                    )
                    refinement = self._call_gemini(refinement_prompt)
                    state["findings"][f"refinement_{iteration + 1}"] = refinement

            state["status"] = "completed"

        except Exception as exc:
            state["status"] = "failed"
            state["error"] = str(exc)

    # ------------------------------------------------------------------ #
    #  Helpers                                                            #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _build_prompt(
        repository_url: str,
        focus_areas: Optional[List[str]],
        current: int,
        total: int,
    ) -> str:
        areas = focus_areas or ["architecture", "performance", "security"]
        return (
            "You are an autonomous code architect analysing a software repository.\n\n"
            f"Repository: {repository_url}\n"
            f"Focus areas: {', '.join(areas)}\n"
            f"Iteration: {current}/{total}\n\n"
            "Please provide:\n"
            "1. Architecture analysis\n"
            "2. Performance bottlenecks\n"
            "3. Security concerns\n"
            "4. Code quality issues\n"
            "5. Specific refactoring recommendations with code examples\n\n"
            "Focus on actionable, specific recommendations that could be implemented."
        )

    def _call_gemini(self, prompt: str) -> str:
        """Synchronous Gemini API call."""
        model = genai.GenerativeModel(self.model_name)
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": 4096,
            },
        )
        return response.text

    @staticmethod
    def _extract_recommendations(response: str) -> List[str]:
        """Pull actionable recommendations from a Gemini response."""
        keywords = ("recommend", "suggest", "should", "consider")
        recs: List[str] = []
        for line in response.split("\n"):
            if any(kw in line.lower() for kw in keywords):
                cleaned = line.strip("- •*").strip()
                if cleaned and len(cleaned) > 10:
                    recs.append(cleaned)
        return recs
