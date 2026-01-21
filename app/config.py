from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    # Database - will use PostgreSQL in production
    database_url: str = Field(
        default="sqlite:///./marketing_budget.db",
        description="Database connection string"
    )
    
    # FastAPI
    app_title: str = "UTAK Marketing Budget System"
    app_version: str = "1.0.0"
    debug: bool = Field(default=True)
    
    # Streamlit
    streamlit_port: int = 8501
    api_base_url: str = Field(
        default="http://localhost:8000",
        description="FastAPI base URL"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = False  # DATABASE_URL and database_url both work

settings = Settings()