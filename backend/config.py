import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    PORT = int(os.getenv("PORT", 8000))
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    
    # Agent Configuration
    MAX_ANALYSIS_DEPTH = 5
    TIMEOUT_SECONDS = 300
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Gemini Configuration
    GEMINI_MODEL = "gemini-3-pro"  # Update as per Gemini 3 model name
    GEMINI_THINKING_LEVEL = "deep"  # For Marathon Agent track
