"""Управление сессиями базы данных"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import settings

# Создание движка БД
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Проверка соединения перед использованием
    echo=settings.debug  # Логирование SQL запросов в debug режиме
)

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency для FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

