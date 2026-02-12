from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class AnalysisStatus(str, Enum):
    PENDING = "pending"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"

class RepositoryInput(BaseModel):
    """Model for repository analysis request"""
    repository_url: str
    branch: str = "main"
    focus_areas: Optional[List[str]] = None  # e.g., ["performance", "security", "architecture"]
    depth: int = 3  # Marathon Agent depth

class AnalysisResponse(BaseModel):
    """Model for analysis response"""
    analysis_id: str
    status: AnalysisStatus
    repository_url: str
    findings: Optional[dict] = None
    recommendations: Optional[List[str]] = None
    generated_code: Optional[List[dict]] = None

class GeminiThinkingConfig(BaseModel):
    """Configuration for Gemini thinking levels"""
    thinking_level: str = "deep"  # For Marathon Agent capabilities
    budget_tokens: int = 8000
    max_iterations: int = 5
