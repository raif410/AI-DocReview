# Запуск DocReview AI Server

## ✅ API ключ настроен!

Ваш OpenAI API ключ успешно сохранен в `.env` файле.

## 🚀 Запуск сервера

### Вариант 1: Через run.py (рекомендуется)

```bash
python run.py
```

### Вариант 2: Напрямую через uvicorn

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Вариант 3: Через Python модуль

```bash
python -m src.main
```

## 📋 Проверка работы

После запуска откройте в браузере:

- **API**: http://localhost:8000
- **Документация (Swagger)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🧪 Тестирование

Запустите тестовый скрипт:

```bash
python scripts/tools/test_example.py
```

Или вручную через curl:

```bash
# Health check
curl http://localhost:8000/health

# Запуск анализа
curl -X POST "http://localhost:8000/api/v1/review/start" \
  -H "Content-Type: application/json" \
  -d '{
    "document": "# Test Document\n\nSome content here",
    "document_type": "markdown"
  }'
```

## ⚠️ Важно

- `.env` файл уже в `.gitignore` и не будет закоммичен
- Сервер запускается на порту 8000
- Для работы требуется активное подключение к интернету (для OpenAI API)

