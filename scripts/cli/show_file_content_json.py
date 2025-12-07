"""Скрипт для показа содержимого файла из C:\review в правильном JSON формате для Swagger UI"""
import sys
import io
import json
from pathlib import Path

# Настройка кодировки для Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

REVIEW_FOLDER = r"C:\review"

def show_file_content_json():
    """Показывает содержимое файлов из C:\review в правильном JSON формате"""
    folder = Path(REVIEW_FOLDER)
    
    if not folder.exists():
        print(f"❌ Папка {REVIEW_FOLDER} не существует!")
        return
    
    # Ищем все .md и .txt файлы
    md_files = list(folder.glob("*.md"))
    txt_files = list(folder.glob("*.txt"))
    all_files = md_files + txt_files
    
    if not all_files:
        print(f"❌ В папке {REVIEW_FOLDER} не найдено файлов .md или .txt")
        print(f"\nПоложите файл в папку: {REVIEW_FOLDER}")
        return
    
    print("=" * 70)
    print("Содержимое файлов из C:\\review (JSON формат для Swagger UI)")
    print("=" * 70)
    
    # Читаем все файлы
    documents = []
    for file_path in sorted(all_files):
        try:
            content = file_path.read_text(encoding="utf-8")
            documents.append(f"# {file_path.name}\n\n{content}")
            print(f"✅ Загружен: {file_path.name}")
        except Exception as e:
            print(f"❌ Ошибка чтения {file_path.name}: {e}")
    
    if not documents:
        return
    
    # Объединяем все файлы
    document = "\n\n---\n\n".join(documents)
    
    # Создаем правильный JSON объект
    request_body = {
        "document": document,
        "document_type": "markdown",
        "context": {}
    }
    
    # Конвертируем в JSON строку (с правильным экранированием)
    # json.dumps() автоматически экранирует:
    # - Двойные кавычки: " -> \"
    # - Переносы строк: \n -> \\n
    # - Обратные слеши: \ -> \\
    # - Управляющие символы: все специальные символы
    json_string = json.dumps(request_body, ensure_ascii=False, indent=2)
    
    # Проверяем валидность JSON
    try:
        parsed = json.loads(json_string)
        print("✅ JSON валиден (все символы правильно экранированы)")
        
        # Проверяем наличие проблемных символов
        issues = []
        if document.count('"') > 0 and '\\"' not in json_string:
            # Это нормально - json.dumps правильно экранирует
            pass
        
        # Подсчитываем экранированные символы
        escaped_quotes = json_string.count('\\"')
        newlines = json_string.count('\\n')
        
        if escaped_quotes > 0:
            print(f"✅ Двойные кавычки экранированы: {escaped_quotes} раз")
        if newlines > 0:
            print(f"✅ Переносы строк экранированы: {newlines} раз")
            
    except json.JSONDecodeError as e:
        print(f"❌ Ошибка валидации JSON: {e}")
        print(f"   Позиция ошибки: {e.pos}")
        print("   Рекомендуется использовать: python send_review_request.py")
        return
    
    print("-" * 70)
    print("\n📄 JSON ДЛЯ КОПИРОВАНИЯ В SWAGGER UI:\n")
    print("=" * 70)
    print(json_string)
    print("=" * 70)
    
    print(f"\n✅ Размер документации: {len(document)} символов")
    print(f"✅ Размер JSON: {len(json_string)} символов")
    print(f"✅ Файлов: {len(all_files)}")
    
    print("\n💡 Инструкция для Swagger UI:")
    print("   1. Выделите весь JSON выше (от '{' до '}')")
    print("   2. Скопируйте (Ctrl+C)")
    print("   3. Откройте http://localhost:8000/docs")
    print("   4. Найдите POST /api/v1/review/start")
    print("   5. Нажмите 'Try it out'")
    print("   6. В поле 'Request body' выберите формат 'application/json'")
    print("   7. Вставьте скопированный JSON (Ctrl+V)")
    print("   8. Нажмите 'Execute'")
    
    print("\n⚠️  ВАЖНО:")
    print("   - Копируйте весь JSON объект целиком (от '{' до '}')")
    print("   - Убедитесь, что выбран формат 'application/json'")
    print("   - Если все равно ошибка 422, используйте: python send_review_request.py")
    print("     (этот скрипт автоматически правильно экранирует все символы)")

if __name__ == "__main__":
    show_file_content_json()

