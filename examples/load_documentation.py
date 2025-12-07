"""Примеры загрузки документации для анализа"""

import requests
from pathlib import Path
import os

BASE_URL = "http://localhost:8000"


def example_1_read_single_file():
    """Пример 1: Чтение из одного файла"""
    print("Пример 1: Чтение из одного файла")
    
    # Читаем файл
    with open("docs/architecture.md", "r", encoding="utf-8") as f:
        document = f.read()
    
    # Отправляем на анализ
    response = requests.post(
        f"{BASE_URL}/api/v1/review/start",
        json={
            "document": document,
            "document_type": "markdown",
            "context": {"project_type": "microservices"}
        }
    )
    
    return response.json()


def example_2_read_multiple_files():
    """Пример 2: Чтение нескольких файлов"""
    print("Пример 2: Чтение нескольких файлов")
    
    # Список файлов для анализа
    files = [
        "docs/architecture.md",
        "docs/api.md",
        "docs/security.md"
    ]
    
    # Читаем и объединяем
    documents = []
    for file_path in files:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                documents.append(f"# {Path(file_path).name}\n\n{content}")
    
    document = "\n\n---\n\n".join(documents)
    
    # Отправляем на анализ
    response = requests.post(
        f"{BASE_URL}/api/v1/review/start",
        json={
            "document": document,
            "document_type": "markdown",
            "context": {"project_type": "microservices"}
        }
    )
    
    return response.json()


def example_3_read_directory():
    """Пример 3: Чтение всех файлов из директории"""
    print("Пример 3: Чтение всех файлов из директории")
    
    docs_dir = Path("docs")
    document = ""
    
    # Читаем все .md файлы
    for md_file in sorted(docs_dir.glob("**/*.md")):
        if md_file.is_file():
            content = md_file.read_text(encoding="utf-8")
            document += f"\n\n# {md_file.relative_to(docs_dir)}\n\n{content}\n\n---\n"
    
    # Отправляем на анализ
    response = requests.post(
        f"{BASE_URL}/api/v1/review/start",
        json={
            "document": document,
            "document_type": "markdown",
            "context": {"project_type": "microservices"}
        }
    )
    
    return response.json()


def example_4_direct_string():
    """Пример 4: Прямая строка"""
    print("Пример 4: Прямая строка")
    
    document = """
# Архитектура платежной системы

## Компоненты
- API Gateway
- Payment Service
- Database

## Безопасность
- Использование HTTPS
- Хранение паролей в открытом виде (⚠️ ПРОБЛЕМА!)

## Требования
Система должна обрабатывать платежи.

## Мониторинг
Не описан.
"""
    
    # Отправляем на анализ
    response = requests.post(
        f"{BASE_URL}/api/v1/review/start",
        json={
            "document": document,
            "document_type": "markdown",
            "context": {
                "project_type": "payment_system",
                "requirements": ["security", "monitoring"]
            }
        }
    )
    
    return response.json()


def example_5_from_environment():
    """Пример 5: Из переменной окружения"""
    print("Пример 5: Из переменной окружения")
    
    # Читаем из переменной окружения
    document = os.getenv("DOCUMENTATION_CONTENT", "")
    
    if not document:
        # Или из файла, указанного в переменной
        doc_path = os.getenv("DOCUMENTATION_PATH", "docs/README.md")
        if os.path.exists(doc_path):
            with open(doc_path, "r", encoding="utf-8") as f:
                document = f.read()
    
    if not document:
        print("Ошибка: Документация не найдена")
        return None
    
    # Отправляем на анализ
    response = requests.post(
        f"{BASE_URL}/api/v1/review/start",
        json={
            "document": document,
            "document_type": "markdown",
            "context": {"project_type": "microservices"}
        }
    )
    
    return response.json()


def example_6_filtered_files():
    """Пример 6: Чтение с фильтрацией"""
    print("Пример 6: Чтение с фильтрацией")
    
    docs_dir = Path("docs")
    document = ""
    
    # Исключаем определенные файлы
    exclude_patterns = ["README.md", "*.example.md"]
    exclude_dirs = ["examples", "tests"]
    
    for md_file in sorted(docs_dir.glob("**/*.md")):
        # Пропускаем исключенные файлы
        if any(pattern in md_file.name for pattern in exclude_patterns):
            continue
        
        # Пропускаем исключенные директории
        if any(exclude_dir in md_file.parts for exclude_dir in exclude_dirs):
            continue
        
        if md_file.is_file():
            content = md_file.read_text(encoding="utf-8")
            document += f"\n\n# {md_file.relative_to(docs_dir)}\n\n{content}\n\n---\n"
    
    # Отправляем на анализ
    response = requests.post(
        f"{BASE_URL}/api/v1/review/start",
        json={
            "document": document,
            "document_type": "markdown",
            "context": {"project_type": "microservices"}
        }
    )
    
    return response.json()


if __name__ == "__main__":
    print("=" * 60)
    print("Примеры загрузки документации")
    print("=" * 60)
    
    # Выберите пример для запуска
    examples = {
        "1": example_1_read_single_file,
        "2": example_2_read_multiple_files,
        "3": example_3_read_directory,
        "4": example_4_direct_string,
        "5": example_5_from_environment,
        "6": example_6_filtered_files,
    }
    
    print("\nДоступные примеры:")
    for key, func in examples.items():
        print(f"  {key}. {func.__doc__}")
    
    choice = input("\nВыберите пример (1-6) или 'all' для всех: ").strip()
    
    if choice == "all":
        for key, func in examples.items():
            try:
                result = func()
                if result:
                    print(f"\n✅ Пример {key}: Task ID = {result.get('task_id')}")
            except Exception as e:
                print(f"\n❌ Пример {key}: Ошибка - {e}")
    elif choice in examples:
        try:
            result = examples[choice]()
            if result:
                print(f"\n✅ Task ID: {result.get('task_id')}")
                print(f"   Status: {result.get('status')}")
                print(f"   Estimated time: {result.get('estimated_time')} seconds")
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")
    else:
        print("Неверный выбор")

