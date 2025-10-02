from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database - will use PostgreSQL in production
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./marketing_budget.db")
    
    # FastAPI
    app_title: str = "Marketing Budget Management System"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Streamlit
    streamlit_port: int = 8501
    api_base_url: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    
    class Config:
        env_file = ".env"

settings = Settings()