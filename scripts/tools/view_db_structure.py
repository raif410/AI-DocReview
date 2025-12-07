"""Скрипт для просмотра структуры базы данных"""
import sys
import io
import os
from pathlib import Path

# Добавляем корень проекта в путь
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import inspect
from src.db.session import engine, SessionLocal
from src.db.models import ReviewTaskDB, IssueDB, ReviewResultDB
from src.config import settings

# Настройка кодировки для Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def print_table_structure(table_name, mapper):
    """Выводит структуру таблицы"""
    print(f"\n{'='*70}")
    print(f"Таблица: {table_name}")
    print(f"{'='*70}")
    
    # Получаем информацию о колонках
    columns = mapper.columns
    
    print(f"\nКолонки ({len(columns)}):")
    print("-" * 70)
    print(f"{'Имя':<30} {'Тип':<25} {'Nullable':<10} {'Default':<15}")
    print("-" * 70)
    
    for col in columns:
        col_type = str(col.type)
        nullable = "YES" if col.nullable else "NO"
        default = str(col.default) if col.default else "-"
        
        # Упрощаем отображение default
        if "Sequence" in default or "ColumnDefault" in default:
            default = "auto"
        elif "callable" in default.lower():
            default = "function"
        
        print(f"{col.name:<30} {col_type:<25} {nullable:<10} {default:<15}")
    
    # Получаем индексы
    indexes = [idx for idx in mapper.table.indexes]
    if indexes:
        print(f"\nИндексы ({len(indexes)}):")
        print("-" * 70)
        for idx in indexes:
            cols = ", ".join([col.name for col in idx.columns])
            unique = "UNIQUE" if idx.unique else ""
            print(f"  {idx.name}: ({cols}) {unique}")
    
    # Получаем первичные ключи
    pk_columns = [col.name for col in mapper.primary_key]
    if pk_columns:
        print(f"\nПервичный ключ: {', '.join(pk_columns)}")
    
    # Получаем внешние ключи
    fk_columns = []
    for col in columns:
        for fk in col.foreign_keys:
            fk_columns.append(f"{col.name} -> {fk.column.table.name}.{fk.column.name}")
    
    if fk_columns:
        print(f"\nВнешние ключи:")
        for fk in fk_columns:
            print(f"  {fk}")


def view_database_structure():
    """Показывает структуру всей базы данных"""
    print("=" * 70)
    print("СТРУКТУРА БАЗЫ ДАННЫХ")
    print("=" * 70)
    print(f"\nПодключение: {settings.database_url.split('@')[1] if '@' in settings.database_url else settings.database_url}")
    
    try:
        # Проверяем подключение
        with engine.connect() as conn:
            print("✅ Подключение к БД успешно")
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")
        print(f"\nПроверьте:")
        print(f"  1. Запущен ли PostgreSQL")
        print(f"  2. Правильно ли настроен DATABASE_URL в .env")
        print(f"  3. Существует ли база данных")
        return
    
    # Получаем inspector для получения информации о таблицах
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    print(f"\nНайдено таблиц в БД: {len(existing_tables)}")
    if existing_tables:
        print(f"Таблицы: {', '.join(existing_tables)}")
    
    # Показываем структуру каждой модели
    models = [
        ("review_tasks", ReviewTaskDB),
        ("issues", IssueDB),
        ("review_results", ReviewResultDB),
    ]
    
    for table_name, model in models:
        if table_name in existing_tables:
            print_table_structure(table_name, model.__mapper__)
        else:
            print(f"\n⚠️  Таблица '{table_name}' не существует в БД")
            print("   Запустите миграции: alembic upgrade head")
            print("   Или инициализируйте БД: python scripts/init_db.py")
    
    print(f"\n{'='*70}")
    print("Для просмотра данных используйте: python scripts/tools/view_db_data.py")
    print(f"{'='*70}")


if __name__ == "__main__":
    view_database_structure()

