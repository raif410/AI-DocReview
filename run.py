"""Скрипт для запуска приложения"""
import os
import sys

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Проверяем наличие OPENAI_API_KEY
if not os.getenv("OPENAI_API_KEY"):
    print("⚠️  ВНИМАНИЕ: OPENAI_API_KEY не установлен!")
    print("Установите переменную окружения или создайте .env файл")
    print("Пример: export OPENAI_API_KEY='your-key-here'")
    print("\nПродолжаем запуск, но функциональность будет ограничена...")

if __name__ == "__main__":
    from src.main import app
    import uvicorn
    from src.config import settings
    
    print(f"🚀 Запуск DocReview AI API на http://{settings.api_host}:{settings.api_port}")
    print(f"📚 Документация: http://{settings.api_host}:{settings.api_port}/docs")
    
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )

