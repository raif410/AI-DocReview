"""Комплексная проверка работоспособности проекта"""
import requests
import sys
import io
import os
import importlib.util

# Настройка кодировки для Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_URL = "http://localhost:8000"
TIMEOUT = 5

def check_mark():
    """Возвращает маркер для статуса"""
    return "[OK]" if True else "[FAIL]"

def check_imports():
    """Проверка импортов основных модулей"""
    print("\n1. Проверка импортов модулей...")
    modules = [
        "src.config",
        "src.models",
        "src.core.director.director",
        "src.core.critic.critic",
        "src.core.synthesizer.synthesizer",
        "src.agents.agent_factory",
        "src.api.main"
    ]
    
    failed = []
    for module in modules:
        try:
            spec = importlib.util.find_spec(module)
            if spec is None:
                print(f"  [FAIL] {module} - не найден")
                failed.append(module)
            else:
                print(f"  [OK]   {module}")
        except Exception as e:
            print(f"  [FAIL] {module} - ошибка: {e}")
            failed.append(module)
    
    return len(failed) == 0

def check_config():
    """Проверка конфигурации"""
    print("\n2. Проверка конфигурации...")
    try:
        from src.config import settings
        print(f"  [OK]   API Title: {settings.api_title}")
        print(f"  [OK]   API Version: {settings.api_version}")
        print(f"  [OK]   Debug Mode: {settings.debug}")
        
        # Проверка API ключа (может быть не установлен)
        if settings.openai_api_key:
            masked_key = settings.openai_api_key[:10] + "..." if len(settings.openai_api_key) > 10 else "***"
            print(f"  [OK]   OpenAI API Key: {masked_key} (установлен)")
        else:
            print(f"  [WARN] OpenAI API Key: не установлен (будет использован мок-режим)")
        
        return True
    except Exception as e:
        print(f"  [FAIL] Ошибка загрузки конфигурации: {e}")
        return False

def check_server_running():
    """Проверка доступности сервера"""
    print("\n3. Проверка доступности сервера...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"  [OK]   Сервер доступен на {BASE_URL}")
            print(f"  [OK]   Статус: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"  [FAIL] Сервер вернул код {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"  [FAIL] Не удалось подключиться к {BASE_URL}")
        print(f"  [INFO] Убедитесь, что сервер запущен: python run.py")
        return False
    except Exception as e:
        print(f"  [FAIL] Ошибка: {e}")
        return False

def check_api_endpoints():
    """Проверка API endpoints"""
    print("\n4. Проверка API endpoints...")
    
    endpoints = [
        ("GET", "/", "Root endpoint"),
        ("GET", "/health", "Health check"),
    ]
    
    all_ok = True
    for method, path, desc in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{path}", timeout=TIMEOUT)
            else:
                continue
            
            if response.status_code < 400:
                print(f"  [OK]   {method} {path} - {desc}")
            else:
                print(f"  [FAIL] {method} {path} - код {response.status_code}")
                all_ok = False
        except Exception as e:
            print(f"  [FAIL] {method} {path} - ошибка: {e}")
            all_ok = False
    
    return all_ok

def check_review_workflow():
    """Проверка рабочего процесса анализа"""
    print("\n5. Проверка рабочего процесса анализа...")
    
    test_document = """# Тестовая документация
    
## Описание
Простая тестовая документация для проверки работы системы.

## Компоненты
- Компонент 1
- Компонент 2

## Безопасность
Требуется добавить проверки безопасности.
"""
    
    try:
        # Создание задачи
        print("  [INFO] Создание тестовой задачи...")
        response = requests.post(
            f"{BASE_URL}/api/v1/review/start",
            json={
                "document": test_document,
                "document_type": "markdown",
                "context": {"test": True}
            },
            timeout=TIMEOUT
        )
        
        if response.status_code != 200:
            print(f"  [FAIL] Не удалось создать задачу: {response.status_code}")
            print(f"  [INFO] Ответ: {response.text[:200]}")
            return False
        
        data = response.json()
        task_id = data.get("task_id")
        if not task_id:
            print(f"  [FAIL] Задача создана, но task_id отсутствует")
            return False
        
        print(f"  [OK]   Задача создана: {task_id}")
        print(f"  [OK]   Статус: {data.get('status')}")
        print(f"  [OK]   Ожидаемое время: {data.get('estimated_time')} сек")
        
        # Проверка статуса
        import time
        time.sleep(1)  # Небольшая задержка
        
        print("  [INFO] Проверка статуса задачи...")
        status_response = requests.get(
            f"{BASE_URL}/api/v1/review/{task_id}/status",
            timeout=TIMEOUT
        )
        
        if status_response.status_code == 200:
            status_data = status_response.json()
            print(f"  [OK]   Статус задачи: {status_data.get('status')}")
            print(f"  [OK]   Есть результат: {status_data.get('has_result', False)}")
            return True
        else:
            print(f"  [WARN] Не удалось получить статус: {status_response.status_code}")
            return False
            
    except Exception as e:
        print(f"  [FAIL] Ошибка при проверке рабочего процесса: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_files():
    """Проверка наличия важных файлов"""
    print("\n6. Проверка структуры проекта...")
    
    important_files = [
        "requirements.txt",
        "README.md",
        "src/api/main.py",
        "src/config.py",
        "src/models.py",
        ".env"
    ]
    
    all_ok = True
    for file_path in important_files:
        if os.path.exists(file_path):
            print(f"  [OK]   {file_path}")
        else:
            print(f"  [WARN] {file_path} - не найден")
            if file_path == ".env":
                print(f"  [INFO] Создайте .env файл: python create_env.ps1")
            all_ok = False if file_path != ".env" else all_ok
    
    return all_ok

def main():
    print("=" * 70)
    print("Проверка работоспособности проекта DocReview AI")
    print("=" * 70)
    
    results = []
    
    # Проверки
    results.append(("Импорты модулей", check_imports()))
    results.append(("Конфигурация", check_config()))
    results.append(("Сервер запущен", check_server_running()))
    results.append(("API endpoints", check_api_endpoints()))
    results.append(("Рабочий процесс", check_review_workflow()))
    results.append(("Структура проекта", check_files()))
    
    # Итоги
    print("\n" + "=" * 70)
    print("ИТОГИ ПРОВЕРКИ")
    print("=" * 70)
    
    for name, result in results:
        status = "[OK]" if result else "[FAIL]"
        print(f"{status} {name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print("\n" + "-" * 70)
    print(f"Пройдено проверок: {passed}/{total}")
    
    if passed == total:
        print("\n[OK] Все проверки пройдены! Проект работает корректно.")
        return 0
    elif passed >= total - 1:
        print("\n[WARN] Большинство проверок пройдено. Есть незначительные проблемы.")
        return 0
    else:
        print("\n[FAIL] Обнаружены критические проблемы. Проверьте ошибки выше.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

