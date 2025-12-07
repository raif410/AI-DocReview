"""Точка входа в приложение"""
import uvicorn
from src.config import settings

if __name__ == "__main__":
    # Используем строку импорта для поддержки reload
    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )

