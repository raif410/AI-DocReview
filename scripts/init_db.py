"""Скрипт для инициализации базы данных"""
import sys
from pathlib import Path

# Добавляем корень проекта в путь
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.db.base import Base
from src.db.session import engine
from src.config import settings

def init_db():
    """Создание всех таблиц в БД"""
    print(f"Connecting to database: {settings.database_url.split('@')[1] if '@' in settings.database_url else 'local'}")
    print("Creating tables...")
    
    # Создаем все таблицы
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database initialized successfully!")
    print(f"Tables created: {list(Base.metadata.tables.keys())}")

if __name__ == "__main__":
    try:
        init_db()
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

