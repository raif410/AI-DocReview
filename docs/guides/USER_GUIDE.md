# 📖 Руководство пользователя DocReview AI

Полное руководство по использованию системы анализа технической документации.

## 📋 Содержание

1. [Что такое DocReview AI?](#что-такое-docreview-ai)
2. [Быстрый старт](#быстрый-старт)
3. [Как использовать API](#как-использовать-api)
4. [Примеры использования](#примеры-использования)
5. [Рабочий процесс](#рабочий-процесс)
6. [Форматы данных](#форматы-данных)
7. [Часто задаваемые вопросы](#часто-задаваемые-вопросы)

---

## Что такое DocReview AI?

**DocReview AI** - это AI-система для автоматического анализа технической документации. Она выявляет:

- 🚨 **Критические ошибки** (безопасность, архитектура, производительность)
- 💡 **Зоны улучшения** (документация, мониторинг, масштабируемость)
- 📊 **Оценку качества** документации
- ✅ **Конкретные рекомендации** от экспертов

### Кто анализирует документацию?

Система использует 4 экспертных агента:
- **Системный аналитик** - требования, бизнес-процессы
- **Архитектор** - архитектура, масштабируемость
- **DevSecOps** - безопасность, уязвимости
- **DevOps/SRE** - надежность, мониторинг

---

## Быстрый старт

### Шаг 1: Установка

```bash
# Установите зависимости
pip install -r requirements.txt

# Настройте API ключ (см. ../setup/SETUP_API_KEY.md)
# Создайте .env файл с OPENAI_API_KEY
```

### Шаг 2: Запуск сервера

```bash
python run.py
```

Сервер запустится на `http://localhost:8000`

### Шаг 3: Проверка работы

```bash
# Быстрая проверка
python scripts/tools/check_project.py

# Или проверка API
python scripts/tools/test_api_quick.py
```

---

## Как использовать API

### Обзор рабочего процесса

```
1. Отправка документации → 2. Получение task_id → 3. Ожидание анализа → 4. Получение результатов
```

### Шаг 1: Запуск анализа

**Endpoint:** `POST /api/v1/review/start`

#### Как загрузить документацию?

> 💡 **Простое объяснение:** Ваш файл должен быть на вашем компьютере. Вы читаете его содержимое и отправляете через API. Файл НЕ загружается на сервер - только его текст!  
> 📖 **Подробная инструкция:** [HOW_TO_LOAD_FILE.md](HOW_TO_LOAD_FILE.md) - прочитайте сначала это!

**Вариант 1: Чтение из файла (Python)**
```python
# Чтение из одного файла
with open("docs/architecture.md", "r", encoding="utf-8") as f:
    document = f.read()

# Или чтение нескольких файлов
documents = []
for file_path in ["docs/architecture.md", "docs/api.md", "docs/security.md"]:
    with open(file_path, "r", encoding="utf-8") as f:
        documents.append(f.read())
document = "\n\n".join(documents)  # Объединяем файлы
```

**Вариант 2: Прямая строка**
```python
document = """
# Архитектура системы

## Компоненты
- API Gateway
- Database
- Cache
"""
```

**Вариант 3: Чтение из директории**
```python
import os
from pathlib import Path

# Читаем все .md файлы из директории
docs_dir = Path("docs")
document = ""
for md_file in docs_dir.glob("**/*.md"):
    document += f"\n\n# {md_file.name}\n\n"
    document += md_file.read_text(encoding="utf-8")
```

**Вариант 4: Из переменной окружения или конфига**
```python
import os
document = os.getenv("DOCUMENTATION_CONTENT", "")
# или
from config import DOCUMENTATION_PATH
with open(DOCUMENTATION_PATH, "r", encoding="utf-8") as f:
    document = f.read()
```

#### Запрос к API

```python
import requests

# Загружаем документацию (выберите один из вариантов выше)
with open("my_documentation.md", "r", encoding="utf-8") as f:
    document = f.read()

# Отправляем запрос
response = requests.post(
    "http://localhost:8000/api/v1/review/start",
    json={
        "document": document,
        "document_type": "markdown",
        "context": {
            "project_type": "microservices",
            "requirements": ["security", "scalability"]
        }
    }
)

task_id = response.json()["task_id"]
print(f"Task ID: {task_id}")
```

**Ответ:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "started",
  "estimated_time": 180
}
```

**Сохраните `task_id`** - он понадобится для получения результатов!

### Шаг 2: Проверка статуса

**Endpoint:** `GET /api/v1/review/{task_id}/status`

**Ответ:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "in_progress",
  "has_result": false
}
```

**Статусы:**
- `started` - задача создана
- `in_progress` - анализ выполняется
- `completed` - анализ завершен
- `failed` - произошла ошибка

### Шаг 3: Получение результатов

**Endpoint:** `GET /api/v1/review/{task_id}/results`

**Ответ:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "summary": "Найдено 5 критических проблем...",
  "issues_count": 5,
  "quality_score": 7.5,
  "report_json": {...}
}
```

### Шаг 4: Получение отчета

**Endpoint:** `GET /api/v1/review/{task_id}/report?format=markdown`

**Форматы:**
- `markdown` - отчет в формате Markdown
- `json` - структурированный JSON

---

## Примеры использования

### Пример 1: Использование через Python

```python
import requests
import time

BASE_URL = "http://localhost:8000"

# Загружаем документацию из файла
with open("my_documentation.md", "r", encoding="utf-8") as f:
    document = f.read()

# 1. Запуск анализа
response = requests.post(
    f"{BASE_URL}/api/v1/review/start",
    json={
        "document": document,  # Используем загруженную документацию
        "document_type": "markdown",
        "context": {"project_type": "microservices"}
    }
)

task_id = response.json()["task_id"]
print(f"Задача создана: {task_id}")

# 2. Ожидание завершения
while True:
    status = requests.get(f"{BASE_URL}/api/v1/review/{task_id}/status").json()
    if status["has_result"]:
        break
    time.sleep(5)

# 3. Получение результатов
results = requests.get(f"{BASE_URL}/api/v1/review/{task_id}/results").json()
print(f"Найдено проблем: {results['issues_count']}")
print(f"Оценка качества: {results['quality_score']}")

# 4. Получение отчета
report = requests.get(
    f"{BASE_URL}/api/v1/review/{task_id}/report?format=markdown"
).json()
print(report["report"])
```

### Пример 2: Использование через curl

```bash
# 1. Запуск анализа
TASK_ID=$(curl -X POST "http://localhost:8000/api/v1/review/start" \
  -H "Content-Type: application/json" \
  -d '{
    "document": "# Тестовая документация",
    "document_type": "markdown"
  }' | jq -r '.task_id')

echo "Task ID: $TASK_ID"

# 2. Проверка статуса
curl "http://localhost:8000/api/v1/review/$TASK_ID/status"

# 3. Получение результатов
curl "http://localhost:8000/api/v1/review/$TASK_ID/results"

# 4. Получение отчета
curl "http://localhost:8000/api/v1/review/$TASK_ID/report?format=markdown"
```

### Пример 3: Использование готового скрипта

```bash
# Запустите готовый пример
python scripts/tools/test_example.py
```

### Пример 4: Использование через браузер (Swagger UI)

1. Откройте http://localhost:8000/docs
2. Найдите endpoint `POST /api/v1/review/start`
3. Нажмите "Try it out"
4. Введите данные и нажмите "Execute"
5. Скопируйте `task_id` из ответа
6. Используйте другие endpoints для получения результатов

---

## Рабочий процесс

### Типичный сценарий использования

```
┌─────────────────────────────────────────────────────────┐
│ 1. Подготовка документации                              │
│    - Соберите документацию в одном файле                │
│    - Формат: Markdown, текст, или другой                 │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 2. Запуск анализа                                        │
│    POST /api/v1/review/start                            │
│    → Получаете task_id                                   │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 3. Ожидание (2-5 минут)                                 │
│    Периодически проверяйте статус:                       │
│    GET /api/v1/review/{task_id}/status                  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 4. Получение результатов                                │
│    GET /api/v1/review/{task_id}/results                 │
│    → Краткая сводка, количество проблем                 │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 5. Получение полного отчета                             │
│    GET /api/v1/review/{task_id}/report?format=markdown  │
│    → Детальный отчет с рекомендациями                   │
└─────────────────────────────────────────────────────────┘
```

### Время выполнения

- **Небольшая документация** (< 1000 строк): ~2-3 минуты
- **Средняя документация** (1000-5000 строк): ~3-5 минут
- **Большая документация** (> 5000 строк): ~5-10 минут

---

## Форматы данных

### Входные данные

**document_type:**
- `markdown` - Markdown формат (рекомендуется)
- `text` - Обычный текст
- `json` - JSON структура

**context** (опционально):
```json
{
  "project_type": "microservices|monolith|serverless",
  "requirements": ["security", "scalability", "performance"],
  "industry": "finance|healthcare|ecommerce"
}
```

### Выходные данные

**Результаты анализа:**
- `summary` - Краткое резюме
- `issues_count` - Количество найденных проблем
- `quality_score` - Оценка качества (0-10)
- `report_json` - Структурированные данные

**Отчет:**
- `markdown` - Готовый отчет в Markdown
- `json` - Структурированный JSON с деталями

---

## Часто задаваемые вопросы

### Как долго длится анализ?

Обычно 2-5 минут, зависит от размера документации. Проверяйте статус через `GET /api/v1/review/{task_id}/status`.

### Что делать, если задача завершилась с ошибкой?

1. Проверьте логи сервера
2. Убедитесь, что API ключ настроен правильно
3. Проверьте формат входных данных
4. Попробуйте с более простым документом

### Можно ли анализировать несколько документов одновременно?

Да! Каждый запрос создает отдельную задачу. Вы можете запустить несколько анализов параллельно.

### Какой максимальный размер документации?

Технически ограничений нет, но рекомендуется:
- До 10,000 строк - оптимально
- 10,000-50,000 строк - может занять больше времени
- Более 50,000 строк - разбейте на части

### Где посмотреть полную документацию API?

После запуска сервера:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Нужен ли API ключ OpenAI?

Да, для работы AI-функций требуется OpenAI API ключ. Без него система будет работать в мок-режиме (только структура, без реального анализа).

### Как сохранить результаты?

Результаты хранятся в памяти сервера. Для постоянного хранения:
1. Сохраните `task_id` и результаты локально
2. Используйте базу данных (PostgreSQL) - см. `docs/database/README.md`

---

## Полезные ссылки

- **Быстрый старт**: [QUICKSTART.md](QUICKSTART.md)
- **Проверка работоспособности**: [../troubleshooting/CHECK_ME.md](../troubleshooting/CHECK_ME.md)
- **Настройка API ключа**: [../setup/SETUP_API_KEY.md](../setup/SETUP_API_KEY.md)
- **Запуск сервера**: [../setup/START_SERVER.md](../setup/START_SERVER.md)
- **Работа с БД**: [docs/database/README.md](docs/database/README.md)
- **Примеры загрузки документации**: [examples/load_documentation.py](examples/load_documentation.py)

---

## Поддержка

Если у вас возникли вопросы или проблемы:

1. Проверьте [../troubleshooting/HOW_TO_CHECK.md](../troubleshooting/HOW_TO_CHECK.md) для диагностики
2. Посмотрите примеры в `test_example.py`
3. Изучите документацию API в Swagger UI: http://localhost:8000/docs

---

**Удачного использования DocReview AI! 🚀**

