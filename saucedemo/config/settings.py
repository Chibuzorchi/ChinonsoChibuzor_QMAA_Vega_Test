from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Base URLs
    BASE_URL: str = "https://www.saucedemo.com/v1"
    
    # User Credentials
    STANDARD_USER: str
    STANDARD_PASSWORD: str
    LOCKED_OUT_USER: str
    LOCKED_OUT_PASSWORD: str
    PROBLEM_USER: Optional[str] = None
    PROBLEM_PASSWORD: Optional[str] = None
    
    # Test Configuration
    HEADLESS: bool = False
    BROWSER: str = "chromium"
    SLOWMO: int = 0
    TIMEOUT: int = 30000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings() 