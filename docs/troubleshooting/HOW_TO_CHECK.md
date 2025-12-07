# Как проверить, что проект работает

## Быстрая проверка (рекомендуется)

Запустите скрипт комплексной проверки:

```bash
python scripts/tools/check_project.py
```

Скрипт проверит:
- ✅ Импорты всех модулей
- ✅ Конфигурацию приложения
- ✅ Доступность сервера
- ✅ Работу API endpoints
- ✅ Создание задач анализа
- ✅ Структуру проекта

## Ручная проверка

### 1. Убедитесь, что сервер запущен

```bash
python run.py
```

Сервер должен запуститься на `http://localhost:8000`

### 2. Проверьте health endpoint

В другом терминале:

```bash
# PowerShell
curl http://localhost:8000/health

# Или через Python
python -c "import requests; print(requests.get('http://localhost:8000/health').json())"
```

Ожидаемый ответ: `{"status": "healthy"}`

### 3. Быстрая проверка API

```bash
python scripts/tools/test_api_quick.py
```

Проверяет все основные endpoints за несколько секунд.

### 4. Полный тест рабочего процесса

```bash
python scripts/tools/test_example.py
```

Создает задачу анализа и проверяет её статус.

## Что должно работать

✅ **Сервер запускается** без ошибок  
✅ **Health endpoint** отвечает `200 OK`  
✅ **Root endpoint** (`/`) возвращает информацию об API  
✅ **Создание задачи** (`POST /api/v1/review/start`) возвращает `task_id`  
✅ **Статус задачи** (`GET /api/v1/review/{task_id}/status`) возвращает статус  

## Возможные проблемы

### Сервер не запускается

1. Проверьте, что порт 8000 свободен
2. Убедитесь, что установлены все зависимости: `pip install -r requirements.txt`
3. Проверьте наличие `.env` файла с настройками

### API не отвечает

1. Убедитесь, что сервер запущен (`python run.py`)
2. Проверьте, что сервер слушает на `localhost:8000`
3. Проверьте логи сервера на наличие ошибок

### Задачи не создаются

1. Проверьте логи сервера
2. Убедитесь, что все модули импортируются без ошибок
3. Проверьте конфигурацию в `.env` файле

## Дополнительные проверки

### Проверка структуры проекта

```bash
python -c "from src.config import settings; print(settings.api_title)"
```

### Проверка импортов

```bash
python -c "from src.api.main import app; print('OK')"
```

### Проверка конфигурации

```bash
python -c "from src.config import settings; print(f'API: {settings.api_title}, Version: {settings.api_version}')"
```

## Статус проверки

После запуска `check_project.py` вы увидите:

- **[OK]** - проверка пройдена
- **[FAIL]** - критическая ошибка
- **[WARN]** - предупреждение (не критично)

Если все проверки пройдены, проект готов к работе! 🚀

