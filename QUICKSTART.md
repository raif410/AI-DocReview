# Быстрый старт DocReview AI

## Требования

- Python 3.11+
- OpenAI API ключ (получить на https://platform.openai.com/)

## Установка

### 1. Установите зависимости

```bash
pip install -r requirements.txt
```

Или минимальный набор для запуска:

```bash
pip install fastapi uvicorn pydantic pydantic-settings openai
```

### 2. Настройте переменные окружения

Создайте файл `.env` или установите переменные окружения:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Или создайте `.env` файл:

```env
OPENAI_API_KEY=your-api-key-here
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
```

## Запуск

### Вариант 1: Через run.py

```bash
python run.py
```

### Вариант 2: Напрямую

```bash
python -m src.main
```

### Вариант 3: Через uvicorn

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

## Использование

### 1. Проверка работоспособности

```bash
curl http://localhost:8000/health
```

### 2. Запуск анализа документации

```bash
curl -X POST "http://localhost:8000/api/v1/review/start" \
  -H "Content-Type: application/json" \
  -d '{
    "document": "# Архитектура системы\n\n## Компоненты\n- API Gateway\n- Database",
    "document_type": "markdown",
    "context": {"project_type": "microservices"}
  }'
```

### 3. Проверка статуса

```bash
curl http://localhost:8000/api/v1/review/{task_id}/status
```

### 4. Получение результатов

```bash
curl http://localhost:8000/api/v1/review/{task_id}/results
```

### 5. Получение отчета

```bash
curl http://localhost:8000/api/v1/review/{task_id}/report?format=markdown
```

## Тестирование

Запустите тестовый скрипт:

```bash
python test_example.py
```

## Документация API

После запуска сервера откройте в браузере:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker (опционально)

### Запуск через Docker Compose

```bash
# Установите OPENAI_API_KEY в .env
docker-compose up
```

### Сборка образа

```bash
docker build -t docreview-ai .
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key docreview-ai
```

## Структура проекта

```
src/
├── models.py              # Модели данных
├── config.py              # Конфигурация
├── main.py                # Точка входа
├── api/
│   └── main.py           # FastAPI приложение
├── core/                  # Ядро системы
│   ├── director/         # Директор
│   ├── critic/           # Критик
│   └── synthesizer/      # Синтезатор
├── agents/                # Агенты-специалисты
│   ├── analyst/          # Системный аналитик
│   ├── architect/        # Архитектор
│   ├── devsecops/        # DevSecOps
│   └── devops_sre/       # DevOps/SRE
└── utils/
    └── ai_client.py      # Клиент OpenAI
```

## Примечания

- Для работы требуется OpenAI API ключ
- В MVP версии результаты хранятся в памяти (перезапуск очистит данные)
- Для продакшена рекомендуется использовать PostgreSQL и Redis
- Время анализа зависит от размера документации (обычно 2-5 минут)

