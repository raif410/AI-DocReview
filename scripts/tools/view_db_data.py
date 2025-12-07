"""Скрипт для просмотра данных из базы данных"""
import sys
import io
import os
from pathlib import Path
from datetime import datetime

# Добавляем корень проекта в путь
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import desc, func
from src.db.session import SessionLocal
from src.db.models import ReviewTaskDB, IssueDB, ReviewResultDB
from src.config import settings

# Настройка кодировки для Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def format_datetime(dt):
    """Форматирует datetime для вывода"""
    if dt is None:
        return "-"
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return str(dt)


def truncate_text(text, max_length=100):
    """Обрезает текст до максимальной длины"""
    if text is None:
        return "-"
    text = str(text)
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def view_review_tasks(db, limit=10):
    """Показывает задачи на анализ"""
    print("\n" + "=" * 70)
    print("ЗАДАЧИ НА АНАЛИЗ (review_tasks)")
    print("=" * 70)
    
    tasks = db.query(ReviewTaskDB).order_by(desc(ReviewTaskDB.created_at)).limit(limit).all()
    
    if not tasks:
        print("  Нет данных")
        return
    
    print(f"\nНайдено задач: {len(tasks)} (показано последних {limit})")
    print("-" * 70)
    
    for i, task in enumerate(tasks, 1):
        print(f"\n[{i}] Задача ID: {task.id}")
        print(f"    Статус: {task.status}")
        print(f"    Тип документа: {task.document_type}")
        print(f"    Email пользователя: {task.user_email or '-'}")
        print(f"    Создано: {format_datetime(task.created_at)}")
        print(f"    Обновлено: {format_datetime(task.updated_at)}")
        print(f"    Документ (первые 100 символов): {truncate_text(task.document, 100)}")
        if task.context:
            print(f"    Контекст: {task.context}")
    
    total = db.query(ReviewTaskDB).count()
    if total > limit:
        print(f"\n... и еще {total - limit} задач (всего: {total})")


def view_issues(db, limit=20):
    """Показывает найденные проблемы"""
    print("\n" + "=" * 70)
    print("НАЙДЕННЫЕ ПРОБЛЕМЫ (issues)")
    print("=" * 70)
    
    issues = db.query(IssueDB).order_by(desc(IssueDB.created_at)).limit(limit).all()
    
    if not issues:
        print("  Нет данных")
        return
    
    print(f"\nНайдено проблем: {len(issues)} (показано последних {limit})")
    print("-" * 70)
    
    for i, issue in enumerate(issues, 1):
        print(f"\n[{i}] Проблема ID: {issue.id}")
        print(f"    Задача ID: {issue.task_id}")
        print(f"    Агент: {issue.agent}")
        print(f"    Приоритет: {issue.priority}")
        print(f"    Категория: {issue.category}")
        print(f"    Заголовок: {truncate_text(issue.title, 60)}")
        print(f"    Описание: {truncate_text(issue.description, 80)}")
        print(f"    Рекомендация: {truncate_text(issue.recommendation, 80)}")
        if issue.location:
            print(f"    Местоположение: {issue.location}")
        print(f"    Создано: {format_datetime(issue.created_at)}")
    
    total = db.query(IssueDB).count()
    if total > limit:
        print(f"\n... и еще {total - limit} проблем (всего: {total})")


def view_review_results(db, limit=10):
    """Показывает результаты анализа"""
    print("\n" + "=" * 70)
    print("РЕЗУЛЬТАТЫ АНАЛИЗА (review_results)")
    print("=" * 70)
    
    results = db.query(ReviewResultDB).order_by(desc(ReviewResultDB.created_at)).limit(limit).all()
    
    if not results:
        print("  Нет данных")
        return
    
    print(f"\nНайдено результатов: {len(results)} (показано последних {limit})")
    print("-" * 70)
    
    for i, result in enumerate(results, 1):
        print(f"\n[{i}] Результат ID: {result.id}")
        print(f"    Задача ID: {result.task_id}")
        print(f"    Статус: {result.status}")
        print(f"    Оценка качества: {result.quality_score or '-'}")
        print(f"    Резюме: {truncate_text(result.summary, 100)}")
        print(f"    Отчет (Markdown, первые 150 символов): {truncate_text(result.report_markdown, 150)}")
        print(f"    Создано: {format_datetime(result.created_at)}")
    
    total = db.query(ReviewResultDB).count()
    if total > limit:
        print(f"\n... и еще {total - limit} результатов (всего: {total})")


def view_statistics(db):
    """Показывает статистику по БД"""
    print("\n" + "=" * 70)
    print("СТАТИСТИКА")
    print("=" * 70)
    
    tasks_count = db.query(ReviewTaskDB).count()
    issues_count = db.query(IssueDB).count()
    results_count = db.query(ReviewResultDB).count()
    
    # Статистика по статусам задач
    tasks_by_status = db.query(
        ReviewTaskDB.status,
        func.count(ReviewTaskDB.id)
    ).group_by(ReviewTaskDB.status).all()
    
    print(f"\nОбщая статистика:")
    print(f"  Задач на анализ: {tasks_count}")
    print(f"  Найденных проблем: {issues_count}")
    print(f"  Результатов анализа: {results_count}")
    
    if tasks_by_status:
        print(f"\nЗадачи по статусам:")
        for status, count in tasks_by_status:
            print(f"  {status}: {count}")


def view_database_data():
    """Показывает данные из базы данных"""
    print("=" * 70)
    print("ДАННЫЕ ИЗ БАЗЫ ДАННЫХ")
    print("=" * 70)
    print(f"\nПодключение: {settings.database_url.split('@')[1] if '@' in settings.database_url else settings.database_url}")
    
    db = SessionLocal()
    try:
        # Показываем статистику
        view_statistics(db)
        
        # Показываем данные из каждой таблицы
        view_review_tasks(db, limit=10)
        view_issues(db, limit=20)
        view_review_results(db, limit=10)
        
        print("\n" + "=" * 70)
        print("Для просмотра структуры БД используйте: python scripts/tools/view_db_structure.py")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Ошибка при чтении данных: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    view_database_data()

