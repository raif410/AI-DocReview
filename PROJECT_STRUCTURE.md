# 📁 Структура проекта

Проект организован для удобства навигации и поддержки.

## 🗂️ Основная структура

```
.
├── README.md                    # Главная документация проекта
├── run.py                       # Запуск сервера
├── requirements.txt             # Зависимости Python
├── docker-compose.yml           # Docker Compose конфигурация
├── Dockerfile                   # Docker образ
│
├── src/                         # Исходный код приложения
│   ├── api/                     # FastAPI endpoints
│   ├── core/                    # Ядро системы (Director, Critic, Synthesizer)
│   ├── agents/                  # Агенты-специалисты
│   ├── db/                      # Работа с базой данных
│   ├── utils/                   # Утилиты
│   ├── models.py                # Pydantic модели
│   └── config.py                # Конфигурация
│
├── scripts/                     # Вспомогательные скрипты
│   ├── tools/                   # Утилиты и тесты
│   │   ├── test_example.py
│   │   ├── test_api_quick.py
│   │   ├── test_openai_key.py
│   │   └── check_project.py
│   ├── init_db.py               # Инициализация БД
│   └── test_db_field.py         # Тест работы с полями
│
├── docs/                         # Документация
│   ├── guides/                  # Руководства пользователя
│   │   ├── USER_GUIDE.md         # Полное руководство
│   │   ├── QUICKSTART.md         # Быстрый старт
│   │   └── ...
│   ├── troubleshooting/         # Решение проблем
│   │   ├── CHECK_ME.md           # Быстрая проверка
│   │   └── ...
│   ├── setup/                    # Настройка и установка
│   │   ├── SETUP_API_KEY.md      # Настройка API ключа
│   │   └── ...
│   ├── analytics/                # Аналитическая документация
│   ├── presentation/             # Презентации
│   ├── database/                 # Документация БД
│   └── api/                       # API документация
│
├── alembic/                      # Миграции базы данных
├── examples/                     # Примеры использования
└── tests/                        # Тесты
```

## 🚀 Как использовать

### Запуск скриптов

**Важно:** Все скрипты запускаются из корня проекта!

```bash
# Утилиты и тесты
python scripts/tools/check_project.py
python scripts/tools/test_api_quick.py
python scripts/tools/test_openai_key.py
python scripts/tools/test_example.py
```

### Навигация по документации

- **Руководства**: [docs/guides/](docs/guides/)
- **Решение проблем**: [docs/troubleshooting/](docs/troubleshooting/)
- **Настройка**: [docs/setup/](docs/setup/)

## 📝 Принципы организации

1. **Разделение по назначению**: Скрипты разделены на CLI и утилиты
2. **Логическая группировка**: Документация сгруппирована по категориям
3. **Легкая навигация**: README файлы в каждой папке для навигации
4. **Сохранение работоспособности**: Все пути обновлены, импорты работают

## 🔗 Связанные файлы

- [README.md](README.md) - Главная документация
- [scripts/README.md](scripts/README.md) - Документация по скриптам
- [docs/guides/README.md](docs/guides/README.md) - Руководства
- [docs/troubleshooting/README.md](docs/troubleshooting/README.md) - Решение проблем
- [docs/setup/README.md](docs/setup/README.md) - Настройка

