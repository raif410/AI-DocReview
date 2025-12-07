"""Пример использования API"""
import requests
import json
import time
import sys
import io

# Настройка кодировки для Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# URL API
BASE_URL = "http://localhost:8000"

# Пример документации для анализа
test_document = """# Архитектура платежной системы

## Компоненты
- API Gateway
- Payment Service
- Database

## Безопасность
- Использование HTTPS
- Хранение паролей в открытом виде

## Требования
Система должна обрабатывать платежи.

## Мониторинг
Не описан.

## Дополнительная информация
Документация содержит описание системы для обработки платежей.
Требуется добавить мониторинг и улучшить безопасность.
"""

def test_review():
    """Тест анализа документации"""
    print("Starting document analysis...")
    
    # 1. Запускаем анализ
    response = requests.post(
        f"{BASE_URL}/api/v1/review/start",
        json={
            "document": test_document,
            "document_type": "markdown",
            "context": {
                "project_type": "payment_system"
            }
        }
    )
    
    if response.status_code != 200:
        print(f"ERROR: {response.status_code}")
        print(response.text)
        return
    
    data = response.json()
    task_id = data["task_id"]
    print(f"Task created: {task_id}")
    print(f"Estimated time: {data['estimated_time']} seconds")
    
    # 2. Ждем завершения
    print("\nWaiting for analysis to complete...")
    max_wait = 180  # 3 минуты
    waited = 0
    check_interval = 3  # Проверяем каждые 3 секунды
    
    while waited < max_wait:
        time.sleep(check_interval)
        waited += check_interval
        
        try:
            status_response = requests.get(f"{BASE_URL}/api/v1/review/{task_id}/status", timeout=5)
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"Status: {status_data['status']} (waited {waited}s)")
                
                if status_data["has_result"]:
                    print("Analysis completed!")
                    break
        except requests.exceptions.RequestException as e:
            print(f"Error checking status: {e}")
            break
    
    # 3. Получаем результаты
    print("\nGetting results...")
    try:
        results_response = requests.get(f"{BASE_URL}/api/v1/review/{task_id}/results", timeout=10)
        
        if results_response.status_code == 200:
            results = results_response.json()
            print(f"\nAnalysis completed!")
            print(f"Issues found: {results['issues_count']}")
            print(f"Quality score: {results.get('quality_score', 'N/A')}")
            print(f"\nSummary:\n{results['summary']}")
            
            # 4. Получаем отчет
            try:
                report_response = requests.get(
                    f"{BASE_URL}/api/v1/review/{task_id}/report?format=markdown",
                    timeout=10
                )
                
                if report_response.status_code == 200:
                    report = report_response.json()
                    print(f"\nReport (first 500 chars):\n{report['report'][:500]}...")
            except Exception as e:
                print(f"Error getting report: {e}")
        else:
            print(f"ERROR getting results: {results_response.status_code}")
            print(results_response.text)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Проверяем доступность API
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("API is available")
            test_review()
        else:
            print("API is not available")
    except requests.exceptions.ConnectionError:
        print("Cannot connect to API. Make sure server is running on http://localhost:8000")
    except Exception as e:
        print(f"Error: {e}")

