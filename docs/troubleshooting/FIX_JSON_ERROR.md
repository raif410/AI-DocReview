# 🔧 Исправление ошибки JSON в Swagger UI

## ❌ Ошибка, которую вы получили

```
422 Error: Unprocessable Entity
"JSON decode error"
"Invalid control character at"
```

## 🔍 Причина ошибки

Ошибка возникает, когда в тексте документации есть специальные символы (переносы строк, табуляции и т.д.), которые не правильно экранированы для JSON.

## ✅ Решение

### Способ 1: Используйте Swagger UI правильно (РЕКОМЕНДУЕТСЯ)

1. Откройте **http://localhost:8000/docs**
2. Найдите `POST /api/v1/review/start`
3. Нажмите "Try it out"
4. **ВАЖНО:** В поле "Request body" (вверху) выберите `application/json`
5. Заполните поля:
   - `document` - вставьте текст вашей документации
   - `document_type` - укажите `"markdown"`
   - `context` - оставьте `{}`
6. Нажмите "Execute"

Swagger UI автоматически правильно экранирует все символы!

### Способ 2: Используйте Python скрипт

Создайте простой скрипт:

```python
import requests
import json

# Читаем файл
with open("your_document.md", "r", encoding="utf-8") as f:
    document = f.read()

# Отправляем запрос
response = requests.post(
    "http://localhost:8000/api/v1/review/start",
    json={  # requests автоматически правильно экранирует!
        "document": document,
        "document_type": "markdown",
        "context": {}
    }
)

print(f"Task ID: {response.json()['task_id']}")
```

### Способ 3: Исправление вручную

Если используете Swagger UI вручную, убедитесь что:

1. **В Swagger UI выбран правильный формат:**
   - В поле "Request body" должно быть: `application/json`
   - НЕ `text/plain` или другой формат

2. **Используйте правильный формат JSON:**
   ```json
   {
     "document": "ваш текст здесь",
     "document_type": "markdown",
     "context": {}
   }
   ```

---

## ⚠️ Частые ошибки

### Ошибка 1: Неправильный формат Request body

**Проблема:** Выбрано `text/plain` вместо `application/json`

**Решение:** В поле "Request body" выберите `application/json`

### Ошибка 2: Неполный JSON

**Проблема:** Скопирован только текст документа, а не весь JSON объект

**Решение:** Заполните все поля в Swagger UI правильно

### Ошибка 3: Неправильное экранирование

**Проблема:** Специальные символы не экранированы

**Решение:** Используйте Python скрипт с `requests.post(json=...)` - он автоматически правильно экранирует

---

## 🎯 Быстрое решение

**Используйте Swagger UI:**
1. Откройте http://localhost:8000/docs
2. Request body: `application/json`
3. Заполните поля
4. Execute

**Или используйте Python:**
```python
import requests

with open("file.md", "r", encoding="utf-8") as f:
    document = f.read()

response = requests.post(
    "http://localhost:8000/api/v1/review/start",
    json={"document": document, "document_type": "markdown", "context": {}}
)
```

**Готово!** ✅
