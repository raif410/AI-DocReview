"""Пример использования API"""
import requests
import json
import time

# URL API
BASE_URL = "http://localhost:8000"

# Пример документации для анализа
test_document = """
# Архитектура платежной системы

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
"""

def test_review():
    """Тест анализа документации"""
    print("🚀 Запуск анализа документации...")
    
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
        print(f"❌ Ошибка: {response.status_code}")
        print(response.text)
        return
    
    data = response.json()
    task_id = data["task_id"]
    print(f"✅ Задача создана: {task_id}")
    print(f"⏱ Ожидаемое время: {data['estimated_time']} секунд")
    
    # 2. Ждем завершения
    print("\n⏳ Ожидание завершения анализа...")
    max_wait = 300  # 5 минут
    waited = 0
    
    while waited < max_wait:
        time.sleep(5)
        waited += 5
        
        status_response = requests.get(f"{BASE_URL}/api/v1/review/{task_id}/status")
        if status_response.status_code == 200:
            status_data = status_response.json()
            print(f"📊 Статус: {status_data['status']}")
            
            if status_data["has_result"]:
                break
    
    # 3. Получаем результаты
    print("\n📋 Получение результатов...")
    results_response = requests.get(f"{BASE_URL}/api/v1/review/{task_id}/results")
    
    if results_response.status_code == 200:
        results = results_response.json()
        print(f"\n✅ Анализ завершен!")
        print(f"📊 Найдено проблем: {results['issues_count']}")
        print(f"⭐ Оценка качества: {results.get('quality_score', 'N/A')}")
        print(f"\n📝 Резюме:\n{results['summary']}")
        
        # 4. Получаем отчет
        report_response = requests.get(
            f"{BASE_URL}/api/v1/review/{task_id}/report?format=markdown"
        )
        
        if report_response.status_code == 200:
            report = report_response.json()
            print(f"\n📄 Отчет (первые 500 символов):\n{report['report'][:500]}...")
    else:
        print(f"❌ Ошибка получения результатов: {results_response.status_code}")


if __name__ == "__main__":
    # Проверяем доступность API
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API доступен")
            test_review()
        else:
            print("❌ API недоступен")
    except requests.exceptions.ConnectionError:
        print("❌ Не удалось подключиться к API. Убедитесь, что сервер запущен на http://localhost:8000")

