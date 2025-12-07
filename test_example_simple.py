"""Упрощенный тест API - только проверка создания задачи"""
import requests
import sys
import io

# Настройка кодировки для Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_URL = "http://localhost:8000"

# Простой тестовый документ
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
"""

def test_api():
    """Быстрый тест API"""
    print("=" * 60)
    print("Testing DocReview AI API")
    print("=" * 60)
    
    # 1. Проверка health
    print("\n1. Checking health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print(f"   OK: {response.json()}")
        else:
            print(f"   ERROR: Status {response.status_code}")
            return
    except Exception as e:
        print(f"   ERROR: {e}")
        return
    
    # 2. Создание задачи
    print("\n2. Creating review task...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/review/start",
            json={
                "document": test_document,
                "document_type": "markdown",
                "context": {
                    "project_type": "payment_system"
                }
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            task_id = data["task_id"]
            print(f"   OK: Task created")
            print(f"   Task ID: {task_id}")
            print(f"   Estimated time: {data['estimated_time']} seconds")
            print(f"   Status: {data['status']}")
            
            # 3. Проверка статуса
            print("\n3. Checking task status...")
            time.sleep(2)  # Даем время на старт
            
            status_response = requests.get(
                f"{BASE_URL}/api/v1/review/{task_id}/status",
                timeout=5
            )
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"   OK: Status retrieved")
                print(f"   Current status: {status_data['status']}")
                print(f"   Has result: {status_data['has_result']}")
            else:
                print(f"   ERROR: Status {status_response.status_code}")
                print(f"   Response: {status_response.text}")
            
            print("\n" + "=" * 60)
            print("Test completed successfully!")
            print(f"Task is processing. Check status at:")
            print(f"  GET {BASE_URL}/api/v1/review/{task_id}/status")
            print(f"Results will be available at:")
            print(f"  GET {BASE_URL}/api/v1/review/{task_id}/results")
            print("=" * 60)
            
        else:
            print(f"   ERROR: Status {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import time
    test_api()

