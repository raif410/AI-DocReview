"""Точка входа в приложение"""
import uvicorn
from src.config import settings
from src.api.main import app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )

