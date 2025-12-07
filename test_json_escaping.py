"""Тест правильного экранирования JSON для Swagger UI"""
import json
import sys
import io
from pathlib import Path

# Настройка кодировки
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

REVIEW_FOLDER = r"C:\review"

def test_json_escaping():
    """Тестирует правильное экранирование JSON"""
    
    # Загружаем файлы
    folder = Path(REVIEW_FOLDER)
    if not folder.exists():
        print(f"❌ Папка {REVIEW_FOLDER} не существует!")
        return
    
    md_files = list(folder.glob("*.md"))
    txt_files = list(folder.glob("*.txt"))
    all_files = md_files + txt_files
    
    if not all_files:
        print(f"❌ Файлы не найдены")
        return
    
    # Читаем файлы
    documents = []
    for file_path in sorted(all_files):
        content = file_path.read_text(encoding="utf-8")
        documents.append(f"# {file_path.name}\n\n{content}")
    
    document = "\n\n---\n\n".join(documents)
    
    # Создаем запрос
    request_data = {
        "document": document,
        "document_type": "markdown",
        "context": {}
    }
    
    # Создаем JSON с правильным экранированием
    json_string = json.dumps(request_data, ensure_ascii=False, indent=2)
    
    print("=" * 70)
    print("Тест экранирования JSON")
    print("=" * 70)
    
    # Проверяем валидность
    try:
        parsed = json.loads(json_string)
        print("✅ JSON валиден")
        print(f"✅ Размер: {len(json_string)} символов")
        
        # Проверяем, что все кавычки экранированы
        if '\\"' in json_string:
            print("✅ Двойные кавычки правильно экранированы (\\\")")
        else:
            print("ℹ️  Двойных кавычек в документе нет")
        
        # Проверяем переносы строк
        if '\\n' in json_string:
            print("✅ Переносы строк правильно экранированы (\\n)")
        
        # Проверяем обратные слеши
        if '\\\\' in json_string:
            print("✅ Обратные слеши правильно экранированы (\\\\)")
        
        print("\n" + "=" * 70)
        print("JSON для копирования в Swagger UI:")
        print("=" * 70)
        print(json_string)
        print("=" * 70)
        
        print("\n💡 Инструкция:")
        print("   1. Скопируйте весь JSON выше (от '{' до '}')")
        print("   2. В Swagger UI выберите формат 'application/json'")
        print("   3. Вставьте JSON")
        print("   4. Нажмите 'Execute'")
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON невалиден: {e}")
        print(f"   Позиция ошибки: {e.pos}")
        print(f"   Текст вокруг ошибки: {json_string[max(0, e.pos-50):e.pos+50]}")

if __name__ == "__main__":
    test_json_escaping()

