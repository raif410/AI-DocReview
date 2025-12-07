"""Тест API запроса для диагностики ошибки 422"""
import requests
import json
import sys
import io

# Настройка кодировки для Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_URL = "http://localhost:8000"

# Загружаем содержимое из C:\review
from pathlib import Path
review_folder = Path(r"C:\review")
md_files = list(review_folder.glob("*.md"))
txt_files = list(review_folder.glob("*.txt"))
all_files = md_files + txt_files

if not all_files:
    print("❌ Файлы не найдены в C:\\review")
    sys.exit(1)

documents = []
for file_path in sorted(all_files):
    content = file_path.read_text(encoding="utf-8")
    documents.append(f"# {file_path.name}\n\n{content}")

document = "\n\n---\n\n".join(documents)

# Создаем правильный запрос
request_data = {
    "document": document,
    "document_type": "markdown",
    "context": {}
}

print("=" * 70)
print("Тест API запроса")
print("=" * 70)
print(f"\n📄 Размер документа: {len(document)} символов")
print(f"📋 Структура запроса:")
print(f"   - document: строка ({len(document)} символов)")
print(f"   - document_type: 'markdown'")
print(f"   - context: {{}}")

# Проверяем валидность JSON
try:
    json_string = json.dumps(request_data, ensure_ascii=False)
    print(f"\n✅ JSON валиден (размер: {len(json_string)} символов)")
except Exception as e:
    print(f"\n❌ Ошибка создания JSON: {e}")
    sys.exit(1)

# Отправляем запрос
print("\n🚀 Отправка запроса...")
try:
    response = requests.post(
        f"{BASE_URL}/api/v1/review/start",
        json=request_data,
        timeout=10
    )
    
    print(f"📊 Статус ответа: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Запрос успешен!")
        print(f"   Task ID: {result.get('task_id')}")
        print(f"   Status: {result.get('status')}")
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
            
except requests.exceptions.ConnectionError:
    print("❌ Не удалось подключиться к серверу")
    print("   Убедитесь, что сервер запущен: python run.py")
except Exception as e:
    print(f"❌ Ошибка: {e}")

