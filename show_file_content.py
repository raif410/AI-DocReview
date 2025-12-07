"""Скрипт для показа содержимого файла из C:\review для копирования в Swagger UI"""
import sys
import io
from pathlib import Path

# Настройка кодировки для Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

REVIEW_FOLDER = r"C:\review"

def show_file_content():
    """Показывает содержимое файлов из C:\review"""
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
    print("Содержимое файлов из C:\\review")
    print("=" * 70)
    print("\n📋 Скопируйте текст ниже и вставьте в поле 'document' в Swagger UI\n")
    print("-" * 70)
    
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
    
    print("-" * 70)
    print("\n📄 СОДЕРЖИМОЕ ДЛЯ КОПИРОВАНИЯ:\n")
    print("=" * 70)
    print(document)
    print("=" * 70)
    
    print(f"\n✅ Размер: {len(document)} символов")
    print(f"✅ Файлов: {len(all_files)}")
    print("\n💡 Инструкция:")
    print("   1. Выделите весь текст выше (от '=' до '=')")
    print("   2. Скопируйте (Ctrl+C)")
    print("   3. Откройте http://localhost:8000/docs")
    print("   4. Найдите POST /api/v1/review/start")
    print("   5. Нажмите 'Try it out'")
    print("   6. Вставьте скопированный текст в поле 'document'")
    print("   7. В поле 'document_type' введите: markdown")
    print("   8. Нажмите 'Execute'")

if __name__ == "__main__":
    show_file_content()

