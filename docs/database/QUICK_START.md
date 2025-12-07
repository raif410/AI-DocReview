# Быстрый старт: Добавление нового поля в БД

## Минимальная инструкция (5 шагов)

### Шаг 1: Обновите Pydantic модель

В `src/models.py` добавьте поле:

```python
class ReviewTask(BaseModel):
    # ... существующие поля
    user_email: Optional[str] = None  # НОВОЕ ПОЛЕ
```

### Шаг 2: Обновите SQLAlchemy модель

В `src/db/models.py` добавьте поле:

```python
class ReviewTaskDB(Base):
    # ... существующие поля
    user_email = Column(String(255), nullable=True, index=True)
```

### Шаг 3: Создайте миграцию

```bash
alembic revision --autogenerate -m "Add user_email to review_tasks"
```

### Шаг 4: Примените миграцию

```bash
alembic upgrade head
```

### Шаг 5: Проверьте работу

```bash
python scripts/test_db_field.py
```

## Готово! ✅

Поле добавлено и готово к использованию.

---

## Подробная документация

- [Полная инструкция](ADDING_FIELD.md) - детальное описание всех шагов
- [Пример с user_email](EXAMPLE_USER_EMAIL.md) - полный пример с кодом
- [Общая документация по БД](README.md) - обзор работы с БД

