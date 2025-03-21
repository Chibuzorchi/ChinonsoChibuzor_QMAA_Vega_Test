import os
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Base URLs
    BASE_URL: str = os.getenv('BASE_URL', 'https://www.saucedemo.com/v1')
    
    # User Credentials
    STANDARD_USER: str = os.getenv('STANDARD_USER', 'standard_user')
    STANDARD_PASSWORD: str = os.getenv('STANDARD_PASSWORD', 'secret_sauce')
    LOCKED_OUT_USER: str = os.getenv('LOCKED_OUT_USER', 'locked_out_user')
    LOCKED_OUT_PASSWORD: str = os.getenv('LOCKED_OUT_PASSWORD', 'secret_sauce')
    PROBLEM_USER: str = os.getenv('PROBLEM_USER', 'problem_user')
    PROBLEM_PASSWORD: str = os.getenv('PROBLEM_PASSWORD', 'secret_sauce')
    
    # Test Configuration
    HEADLESS: bool = os.getenv('HEADLESS', 'false').lower() == 'true'
    BROWSER: str = os.getenv('BROWSER', 'chromium')
    SLOWMO: int = int(os.getenv('SLOWMO', '0'))
    TIMEOUT: int = int(os.getenv('TIMEOUT', '30000'))
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True
        env_prefix = ''

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    try:
        return Settings()
    except Exception as e:
        # Provide default settings if environment variables are missing
        return Settings(
            BASE_URL='https://www.saucedemo.com/v1',
            STANDARD_USER='standard_user',
            STANDARD_PASSWORD='secret_sauce',
            LOCKED_OUT_USER='locked_out_user',
            LOCKED_OUT_PASSWORD='secret_sauce',
            PROBLEM_USER='problem_user',
            PROBLEM_PASSWORD='secret_sauce',
            HEADLESS=True,
            BROWSER='chromium',
            SLOWMO=0,
            TIMEOUT=30000
        ) 