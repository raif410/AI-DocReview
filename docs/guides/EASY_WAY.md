# 🚀 Самый простой способ отправить запрос

## ✅ Используйте Swagger UI или API напрямую

**Все взаимодействие с системой происходит через REST API.**

## 📋 Варианты использования

### Вариант 1: Swagger UI (рекомендуется)

1. Откройте **http://localhost:8000/docs**
2. Найдите `POST /api/v1/review/start`
3. Нажмите "Try it out"
4. Заполните поля:
   - `document` - вставьте текст вашей документации
   - `document_type` - укажите "markdown"
   - `context` - оставьте `{}` или добавьте контекст
5. Нажмите "Execute"

Подробнее: [SWAGGER_UI_GUIDE.md](SWAGGER_UI_GUIDE.md)

### Вариант 2: Python скрипт

Используйте пример из `examples/load_documentation.py`:

```python
import requests

# Читаем файл
with open("your_document.md", "r", encoding="utf-8") as f:
    document = f.read()

# Отправляем запрос
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

### Вариант 3: cURL

```bash
curl -X POST "http://localhost:8000/api/v1/review/start" \
  -H "Content-Type: application/json" \
  -d '{
    "document": "# Ваша документация здесь...",
    "document_type": "markdown",
    "context": {}
  }'
```

## 🎯 После отправки запроса

Вы получите `task_id`. Затем:

1. Проверьте статус: `GET /api/v1/review/{task_id}/status`
2. Получите результаты: `GET /api/v1/review/{task_id}/results`
3. Получите отчет: `GET /api/v1/review/{task_id}/report?format=markdown`

## ✅ Рекомендация

**Используйте Swagger UI** - это самый простой способ для начала работы! 🎉
