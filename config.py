from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", 8000))
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    model_name: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    
    # Chroma Vector Database
    chroma_db_path: str = os.getenv("CHROMA_DB_PATH", "./data/chroma_db")
    
    # MindMate Website URLs for Knowledge Base
    mindmate_website_urls: List[str] = []
    
    # Counselor Scheduling
    counselor_booking_link: str = os.getenv("COUNSELOR_BOOKING_LINK", "")
    
    # Stress Detection Thresholds
    stress_level_threshold: float = 0.7  # Threshold to trigger counselor booking
    pattern_detection_window: int = 5  # Number of messages to track for pattern detection
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
