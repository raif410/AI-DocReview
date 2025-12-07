"""Скрипт для анализа документации из папки C:\review"""
import requests
import time
import os
from pathlib import Path
import sys
import io

# Настройка кодировки для Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_URL = "http://localhost:8000"
REVIEW_FOLDER = r"C:\review"

def load_documents_from_folder(folder_path):
    """Загружает все .md и .txt файлы из указанной папки"""
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"❌ Папка {folder_path} не существует!")
        return None
    
    # Ищем все .md и .txt файлы
    md_files = list(folder.glob("*.md"))
    txt_files = list(folder.glob("*.txt"))
    all_files = md_files + txt_files
    
    if not all_files:
        print(f"❌ В папке {folder_path} не найдено файлов .md или .txt")
        return None
    
    print(f"📁 Найдено файлов: {len(all_files)}")
    
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
        return None
    
    # Объединяем все файлы
    document = "\n\n---\n\n".join(documents)
    print(f"\n📄 Общий размер документации: {len(document)} символов")
    
    return document

def start_review(document, context=None):
    """Запускает анализ документации"""
    print("\n🚀 Запуск анализа документации...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/review/start",
            json={
                "document": document,
                "document_type": "markdown",
                "context": context or {"source": "C:\\review"}
            },
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"❌ Ошибка: {response.status_code}")
            print(response.text)
            return None
        
        data = response.json()
        task_id = data["task_id"]
        print(f"✅ Задача создана: {task_id}")
        print(f"⏱ Ожидаемое время: {data['estimated_time']} секунд")
        
        return task_id
        
    except requests.exceptions.ConnectionError:
        print("❌ Не удалось подключиться к серверу")
        print("   Убедитесь, что сервер запущен: python run.py")
        return None
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def wait_for_completion(task_id, max_wait=300):
    """Ожидает завершения анализа"""
    print("\n⏳ Ожидание завершения анализа...")
    
    waited = 0
    check_interval = 5
    
    while waited < max_wait:
        time.sleep(check_interval)
        waited += check_interval
        
        try:
            status_response = requests.get(
                f"{BASE_URL}/api/v1/review/{task_id}/status",
                timeout=5
            )
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                status = status_data['status']
                print(f"📊 Статус: {status} (прошло {waited}с)")
                
                if status_data["has_result"]:
                    print("✅ Анализ завершен!")
                    return True
                elif status == "failed":
                    print("❌ Анализ завершился с ошибкой")
                    return False
        except Exception as e:
            print(f"⚠️ Ошибка проверки статуса: {e}")
    
    print(f"⏰ Превышено время ожидания ({max_wait}с)")
    return False

def get_results(task_id):
    """Получает результаты анализа"""
    print("\n📋 Получение результатов...")
    
    try:
        results_response = requests.get(
            f"{BASE_URL}/api/v1/review/{task_id}/results",
            timeout=10
        )
        
        if results_response.status_code == 200:
            results = results_response.json()
            print(f"\n✅ Анализ завершен!")
            print(f"📊 Найдено проблем: {results['issues_count']}")
            print(f"⭐ Оценка качества: {results.get('quality_score', 'N/A')}")
            print(f"\n📝 Резюме:\n{results['summary']}")
            
            # Получаем отчет
            try:
                report_response = requests.get(
                    f"{BASE_URL}/api/v1/review/{task_id}/report?format=markdown",
                    timeout=10
                )
                
                if report_response.status_code == 200:
                    report = report_response.json()
                    
                    # Сохраняем отчет в файл
                    report_file = Path(REVIEW_FOLDER) / "review_report.md"
                    report_file.write_text(report['report'], encoding="utf-8")
                    print(f"\n📄 Отчет сохранен: {report_file}")
                    
                    # Показываем первые 500 символов
                    print(f"\n📄 Отчет (первые 500 символов):\n{report['report'][:500]}...")
            except Exception as e:
                print(f"⚠️ Ошибка получения отчета: {e}")
            
            return results
        else:
            print(f"❌ Ошибка получения результатов: {results_response.status_code}")
            print(results_response.text)
            return None
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def main():
    """Главная функция"""
    print("=" * 60)
    print("DocReview AI - Анализ документации из C:\\review")
    print("=" * 60)
    
    # Проверяем доступность сервера
    try:
        health_response = requests.get(f"{BASE_URL}/health", timeout=5)
        if health_response.status_code != 200:
            print("❌ Сервер недоступен")
            return
    except:
        print("❌ Сервер не запущен!")
        print("   Запустите сервер: python run.py")
        return
    
    print("✅ Сервер доступен\n")
    
    # Загружаем документы из папки
    document = load_documents_from_folder(REVIEW_FOLDER)
    
    if not document:
        print("\n❌ Не удалось загрузить документы")
        return
    
    # Запускаем анализ
    task_id = start_review(document)
    
    if not task_id:
        return
    
    # Ждем завершения
    if wait_for_completion(task_id):
        # Получаем результаты
        get_results(task_id)
    else:
        print("\n⚠️ Анализ не завершился в ожидаемое время")
        print(f"   Проверьте статус вручную: GET {BASE_URL}/api/v1/review/{task_id}/status")

if __name__ == "__main__":
    main()

