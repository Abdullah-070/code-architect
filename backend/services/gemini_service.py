import google.generativeai as genai
from config import Config
import asyncio
from typing import Optional, List, Dict
import json

class GeminiService:
    """Service for interacting with Gemini 3 API"""
    
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = Config.GEMINI_MODEL
        self.analysis_cache = {}  # In-memory cache for demo; use Redis in production
    
    async def start_analysis(
        self,
        analysis_id: str,
        repository_url: str,
        branch: str = "main",
        focus_areas: Optional[List[str]] = None,
        depth: int = 3
    ):
        """
        Start autonomous code analysis using Gemini 3 with Marathon Agent capabilities
        """
        try:
            # Initialize analysis state
            analysis_state = {
                "analysis_id": analysis_id,
                "status": "analyzing",
                "repository_url": repository_url,
                "findings": {},
                "recommendations": [],
                "generated_code": [],
                "iteration": 0,
                "max_iterations": depth
            }
            
            # Store in cache
            self.analysis_cache[analysis_id] = analysis_state
            
            # Start async analysis task
            asyncio.create_task(
                self._run_autonomous_analysis(analysis_id, repository_url, focus_areas, depth)
            )
            
            return analysis_state
        except Exception as e:
            raise Exception(f"Failed to start analysis: {str(e)}")
    
    async def _run_autonomous_analysis(
        self,
        analysis_id: str,
        repository_url: str,
        focus_areas: Optional[List[str]],
        depth: int
    ):
        """
        Run the autonomous Marathon Agent analysis loop
        """
        try:
            analysis_state = self.analysis_cache[analysis_id]
            
            for iteration in range(depth):
                analysis_state["iteration"] = iteration + 1
                
                # Build context from repository (simulated - in production, clone and analyze repo)
                repo_context = f"""
                Analyzing repository: {repository_url}
                Focus areas: {focus_areas or ['architecture', 'performance', 'security']}
                Iteration: {iteration + 1}/{depth}
                """
                
                # Call Gemini 3 with extended thinking
                prompt = f"""
                You are an autonomous code architect analyzing a software repository.
                
                Repository Context:
                {repo_context}
                
                Please provide:
                1. Architecture analysis
                2. Performance bottlenecks
                3. Security concerns
                4. Code quality issues
                5. Specific refactoring recommendations with code examples
                
                Focus on actionable, specific recommendations that could be implemented.
                """
                
                # Make API call to Gemini 3
                response = await self._call_gemini(prompt)
                
                # Parse and store findings
                analysis_state["findings"][f"iteration_{iteration + 1}"] = response
                analysis_state["recommendations"].extend(
                    self._extract_recommendations(response)
                )
                
                # Self-correct if needed
                if iteration < depth - 1:
                    refinement_prompt = f"""
                    Based on the previous analysis, please provide:
                    1. What we might have missed
                    2. Deeper architectural insights
                    3. Cross-cutting concerns
                    """
                    refinement = await self._call_gemini(refinement_prompt)
                    analysis_state["findings"][f"refinement_{iteration + 1}"] = refinement
            
            analysis_state["status"] = "completed"
            
        except Exception as e:
            analysis_state["status"] = "failed"
            analysis_state["error"] = str(e)
    
    async def _call_gemini(self, prompt: str) -> str:
        """
        Call Gemini 3 API with Marathon Agent thinking level
        """
        try:
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 40,
                    "max_output_tokens": 4096,
                }
            )
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API call failed: {str(e)}")
    
    def _extract_recommendations(self, response: str) -> List[str]:
        """
        Extract actionable recommendations from Gemini response
        """
        recommendations = []
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['recommend', 'suggest', 'should', 'consider']):
                cleaned = line.strip('- •*').strip()
                if cleaned and len(cleaned) > 10:
                    recommendations.append(cleaned)
        return recommendations
    
    async def get_analysis_result(self, analysis_id: str) -> Optional[Dict]:
        """
        Retrieve analysis result from cache
        """
        return self.analysis_cache.get(analysis_id)
