from pydantic_settings import BaseSettings
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # API configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FlowWork HR Automation"
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-development-only")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutes
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = [
    "http://localhost:3000",  # React frontend
    "http://localhost:8000",  # FastAPI backend
    "http://localhost:5173",  # Vite default dev server
    "http://localhost",
]
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/flowwork")
    
    # File storage
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    
    class Config:
        case_sensitive = True


# Create settings instance
settings = Settings()