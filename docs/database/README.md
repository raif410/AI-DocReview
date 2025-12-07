# Работа с базой данных

## Обзор

Проект использует **PostgreSQL** в качестве основной базы данных и **SQLAlchemy** как ORM. Для управления миграциями используется **Alembic**.

## Структура

```
src/
├── db/
│   ├── __init__.py          # Инициализация БД
│   ├── models.py            # SQLAlchemy модели
│   ├── session.py           # Сессии БД
│   └── base.py              # Базовый класс
├── alembic/                 # Миграции Alembic
│   ├── versions/            # Файлы миграций
│   └── env.py               # Конфигурация Alembic
└── alembic.ini              # Конфигурация Alembic
```

## Быстрый старт

### 1. Установка зависимостей

```bash
pip install sqlalchemy alembic psycopg2-binary
```

### 2. Настройка подключения

В `.env` файле:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/docreview
```

### 3. Инициализация Alembic (если еще не инициализирован)

```bash
alembic init alembic
```

### 4. Создание первой миграции

```bash
alembic revision --autogenerate -m "Initial migration"
```

### 5. Применение миграций

```bash
alembic upgrade head
```

