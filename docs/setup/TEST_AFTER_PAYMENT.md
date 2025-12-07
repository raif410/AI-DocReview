# ✅ Проверка работы после оплаты API

## 🧪 Тестирование

### 1. Проверка API ключа

```bash
python scripts/tools/test_openai_key.py
```

Должен вернуться: `✅ API ключ работает!`

### 2. Проверка API запроса

Используйте Swagger UI или Python:

**Swagger UI:**
1. Откройте http://localhost:8000/docs
2. Найдите `POST /api/v1/review/start`
3. Заполните поля и отправьте запрос

**Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/review/start",
    json={
        "document": "# Тест\n\nЭто тестовая документация.",
        "document_type": "markdown",
        "context": {}
    }
)

print(f"Task ID: {response.json()['task_id']}")
```

## 🔄 Если сервер не перезапущен

**ВАЖНО:** После обновления `.env` нужно перезапустить сервер!

1. Остановите сервер (Ctrl+C)
2. Запустите снова:
   ```bash
   python run.py
   ```

## 🚀 Тестирование через Swagger UI

1. Откройте http://localhost:8000/docs
2. Найдите `POST /api/v1/review/start`
3. Заполните поля:
   - `document`: вставьте текст документации
   - `document_type`: `"markdown"`
   - `context`: `{}`
4. Нажмите "Execute"

## ✅ Ожидаемый результат

После оплаты и перезапуска сервера:
- ✅ API ключ работает
- ✅ Запросы проходят успешно
- ✅ Анализ документации выполняется с реальным AI

Готово! 🎉
