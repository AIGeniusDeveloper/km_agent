import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "KM-Agent FP Multi-Secteurs"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # LLM Configuration
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # Vector DB Configuration
    CHROMA_PERSIST_DIRECTORY: str = os.path.join(os.getcwd(), "km_agent/data/chroma_db")
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
