"""Простой скрипт для отправки запроса на анализ документации"""
import requests
import json
import sys
import io
from pathlib import Path

# Настройка кодировки для Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_URL = "http://localhost:8000"
REVIEW_FOLDER = r"C:\review"

def main():
    """Отправляет запрос на анализ документации"""
    print("=" * 70)
    print("Отправка запроса на анализ документации")
    print("=" * 70)
    
    # Загружаем файлы из C:\review
    folder = Path(REVIEW_FOLDER)
    
    if not folder.exists():
        print(f"❌ Папка {REVIEW_FOLDER} не существует!")
        return
    
    md_files = list(folder.glob("*.md"))
    txt_files = list(folder.glob("*.txt"))
    all_files = md_files + txt_files
    
    if not all_files:
        print(f"❌ В папке {REVIEW_FOLDER} не найдено файлов .md или .txt")
        return
    
    print(f"\n📁 Найдено файлов: {len(all_files)}")
    
    # Читаем все файлы
    documents = []
    for file_path in sorted(all_files):
        try:
            content = file_path.read_text(encoding="utf-8")
            documents.append(f"# {file_path.name}\n\n{content}")
            print(f"  ✅ {file_path.name}")
        except Exception as e:
            print(f"  ❌ Ошибка чтения {file_path.name}: {e}")
    
    if not documents:
        return
    
    # Объединяем все файлы
    document = "\n\n---\n\n".join(documents)
    print(f"\n📄 Размер документации: {len(document)} символов")
    
    # Создаем запрос
    request_data = {
        "document": document,
        "document_type": "markdown",
        "context": {}
    }
    
    # Проверяем доступность сервера
    try:
        health = requests.get(f"{BASE_URL}/health", timeout=5)
        if health.status_code != 200:
            print("❌ Сервер недоступен")
            return
    except:
        print("❌ Не удалось подключиться к серверу")
        print("   Убедитесь, что сервер запущен: python run.py")
        return
    
    print("✅ Сервер доступен")
    
    # Отправляем запрос
    print("\n🚀 Отправка запроса на анализ...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/review/start",
            json=request_data,  # requests автоматически правильно экранирует JSON
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            task_id = result["task_id"]
            print(f"✅ Запрос успешен!")
            print(f"\n📋 Task ID: {task_id}")
            print(f"⏱ Ожидаемое время: {result['estimated_time']} секунд")
            print(f"📊 Статус: {result['status']}")
            
            print(f"\n💡 Проверьте статус:")
            print(f"   GET {BASE_URL}/api/v1/review/{task_id}/status")
            print(f"\n💡 Получите результаты:")
            print(f"   GET {BASE_URL}/api/v1/review/{task_id}/results")
            print(f"\n💡 Или используйте Swagger UI:")
            print(f"   {BASE_URL}/docs")
            
        else:
            print(f"❌ Ошибка: {response.status_code}")
            print(f"   Ответ: {response.text}")
            
            # Пробуем распарсить детали ошибки
            try:
                error_detail = response.json()
                print(f"\n📋 Детали ошибки:")
                print(json.dumps(error_detail, indent=2, ensure_ascii=False))
            except:
                pass
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка запроса: {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")

if __name__ == "__main__":
    main()

