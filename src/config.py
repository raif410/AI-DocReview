"""Конфигурация приложения"""
import os
from typing import Optional

try:
    from pydantic_settings import BaseSettings
except ImportError:
    # Fallback для старых версий pydantic
    from pydantic import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # API
    api_title: str = "DocReview AI API"
    api_version: str = "1.0.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
    
    # OpenAI / DeepSeek
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    openai_temperature: float = 0.3
    openai_max_tokens: int = 2000
    openai_base_url: Optional[str] = None  # Для DeepSeek: https://api.deepseek.com
    
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/docreview"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_cache_ttl: int = 3600
    
    # Agents
    max_iterations: int = 3
    analysis_timeout: int = 300  # секунд
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8-sig"  # Поддержка BOM
        case_sensitive = False
        extra = "ignore"  # Игнорировать лишние поля


settings = Settings()

