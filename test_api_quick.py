"""Быстрая проверка доступности API"""
import requests
import sys
import time
import io

# Настройка кодировки для Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_URL = "http://localhost:8000"
TIMEOUT = 5

def test_endpoint(method, path, description, **kwargs):
    """Тест одного endpoint"""
    url = f"{BASE_URL}{path}"
    try:
        start_time = time.time()
        if method == "GET":
            response = requests.get(url, timeout=TIMEOUT, **kwargs)
        elif method == "POST":
            response = requests.post(url, timeout=TIMEOUT, **kwargs)
        elapsed = (time.time() - start_time) * 1000  # в миллисекундах
        
        status = "OK" if response.status_code < 400 else "ERROR"
        print(f"{status:6} | {method:4} {path:40} | {response.status_code:3} | {elapsed:6.1f}ms | {description}")
        return response.status_code < 400
    except requests.exceptions.ConnectionError:
        print(f"FAIL   | {method:4} {path:40} | --- |   --- | {description} (Connection refused)")
        return False
    except requests.exceptions.Timeout:
        print(f"TIMEOUT| {method:4} {path:40} | --- |   --- | {description} (Timeout)")
        return False
    except Exception as e:
        print(f"ERROR  | {method:4} {path:40} | --- |   --- | {description} ({str(e)[:30]})")
        return False

def main():
    print("=" * 100)
    print("Quick API Health Check")
    print("=" * 100)
    print(f"{'Status':6} | {'Method':4} {'Endpoint':40} | {'Code':3} | {'Time':6} | Description")
    print("-" * 100)
    
    results = []
    
    # 1. Health check
    results.append(test_endpoint("GET", "/health", "Health check"))
    
    # 2. Root endpoint
    results.append(test_endpoint("GET", "/", "Root endpoint"))
    
    # 3. Start review (создаем тестовую задачу)
    test_doc = "# Test Document\nThis is a test."
    results.append(test_endpoint(
        "POST", 
        "/api/v1/review/start",
        "Create review task",
        json={
            "document": test_doc,
            "document_type": "markdown",
            "context": {}
        }
    ))
    
    # 4. Проверяем статус созданной задачи (если она была создана)
    if results[-1]:  # Если последний запрос успешен
        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/review/start",
                json={
                    "document": test_doc,
                    "document_type": "markdown",
                    "context": {}
                },
                timeout=TIMEOUT
            )
            if response.status_code == 200:
                task_id = response.json().get("task_id")
                if task_id:
                    time.sleep(0.5)  # Небольшая задержка
                    results.append(test_endpoint("GET", f"/api/v1/review/{task_id}/status", "Get task status"))
        except:
            pass
    
    # Итоги
    print("-" * 100)
    passed = sum(results)
    total = len(results)
    print(f"\nResults: {passed}/{total} endpoints responding")
    
    if passed == total:
        print("[OK] All endpoints are responding correctly!")
        return 0
    else:
        print("[WARN] Some endpoints are not responding")
        return 1

if __name__ == "__main__":
    sys.exit(main())

