"""Скрипт для запуска приложения"""
import os
import sys

# Настройка кодировки для Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Проверяем наличие OPENAI_API_KEY
if not os.getenv("OPENAI_API_KEY"):
    print("WARNING: OPENAI_API_KEY not set!")
    print("Set environment variable or create .env file")
    print("Example: export OPENAI_API_KEY='your-key-here'")
    print("\nContinuing startup, but functionality will be limited...")

if __name__ == "__main__":
    try:
        import uvicorn
        from src.config import settings
        
        print(f"Starting DocReview AI API on http://{settings.api_host}:{settings.api_port}")
        print(f"Documentation: http://{settings.api_host}:{settings.api_port}/docs")
        print(f"Press CTRL+C to stop")
        
        # Используем строку импорта для поддержки reload
        uvicorn.run(
            "src.api.main:app",
            host=settings.api_host,
            port=settings.api_port,
            reload=settings.debug
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

