# 🚀 Быстрая проверка работы системы

## Шаг 1: Убедитесь, что сервер запущен

Откройте терминал и проверьте:

```bash
curl http://localhost:8000/health
```

Должен вернуться: `{"status":"healthy"}`

**Если сервер не запущен:**
```bash
python run.py
```

Оставьте этот терминал открытым - сервер должен работать.

---

## Шаг 2: Подготовьте документацию

Подготовьте файл с документацией в любом месте на вашем компьютере.

**Пример:**
- `my_docs.md`
- `architecture.md`
- `test.txt`

**Важно:** Файл должен быть в формате `.md` или `.txt`

---

## Шаг 3: Отправьте запрос через Swagger UI

1. Откройте **http://localhost:8000/docs**
2. Найдите `POST /api/v1/review/start`
3. Нажмите "Try it out"
4. Откройте ваш файл, скопируйте содержимое (Ctrl+A, Ctrl+C)
5. Вставьте в поле `document` в Swagger UI
6. Нажмите "Execute"

Подробнее: [SWAGGER_UI_GUIDE.md](SWAGGER_UI_GUIDE.md)

---

## Шаг 4: Или используйте Python скрипт

```python
import requests

# Читаем файл
with open("your_document.md", "r", encoding="utf-8") as f:
    document = f.read()

# Отправляем на анализ
response = requests.post(
    "http://localhost:8000/api/v1/review/start",
    json={
        "document": document,
        "document_type": "markdown",
        "context": {}
    }
)

task_id = response.json()["task_id"]
print(f"Task ID: {task_id}")
```

---

## Шаг 5: Проверьте статус

Используйте Swagger UI или Python:

```python
import requests
import time

task_id = "ваш-task-id-здесь"

while True:
    status = requests.get(
        f"http://localhost:8000/api/v1/review/{task_id}/status"
    ).json()
    
    print(f"Статус: {status['status']}")
    
    if status["has_result"]:
        break
    
    time.sleep(5)
```

---

## Шаг 6: Получите результаты

```python
results = requests.get(
    f"http://localhost:8000/api/v1/review/{task_id}/results"
).json()

print(f"Найдено проблем: {results['issues_count']}")
print(f"Оценка: {results['quality_score']}")
print(f"Резюме: {results['summary']}")
```

---

## Если что-то пошло не так

### Ошибка: "Сервер не запущен"
**Решение:** Запустите сервер: `python run.py`

### Ошибка: "Не удалось подключиться"
**Решение:** Убедитесь, что сервер запущен и доступен на `http://localhost:8000`

### Анализ долго выполняется
**Это нормально!** Анализ может занять 2-5 минут. Просто подождите.

---

## Готово! 🎉

Теперь вы знаете, как проверить работу системы через API!
