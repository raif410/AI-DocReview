# Добавление нового поля в базу данных

## Пошаговая инструкция

Это руководство покажет, как добавить новое поле в базу данных на примере добавления поля `user_email` в таблицу `review_tasks`.

---

## Шаг 1: Обновление Pydantic модели

Сначала обновим Pydantic модель в `src/models.py`:

```python
class ReviewTask(BaseModel):
    """Задача на анализ документации"""
    id: UUID = Field(default_factory=uuid4)
    document: str
    document_type: str = "markdown"
    context: Dict[str, Any] = Field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # НОВОЕ ПОЛЕ
    user_email: Optional[str] = None  # Email пользователя, создавшего задачу
```

**Важно**: 
- Используйте `Optional[тип]` для необязательных полей
- Для обязательных полей просто укажите тип без `Optional`
- Установите значение по умолчанию (`= None` или другое)

---

## Шаг 2: Обновление SQLAlchemy модели

Создайте или обновите SQLAlchemy модель в `src/db/models.py`:

```python
from sqlalchemy import Column, String, DateTime, Text, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class ReviewTaskDB(Base):
    """SQLAlchemy модель для ReviewTask"""
    __tablename__ = "review_tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document = Column(Text, nullable=False)
    document_type = Column(String(50), default="markdown")
    context = Column(JSON, default=dict)
    status = Column(SQLEnum('pending', 'in_progress', 'completed', 'failed'), default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # НОВОЕ ПОЛЕ
    user_email = Column(String(255), nullable=True, index=True)  # Email пользователя
```

**Типы данных SQLAlchemy**:
- `String(255)` - VARCHAR(255)
- `Text` - TEXT (для больших текстов)
- `Integer` - INTEGER
- `Boolean` - BOOLEAN
- `DateTime` - TIMESTAMP
- `JSON` - JSONB (PostgreSQL)
- `UUID` - UUID (PostgreSQL)

**Параметры**:
- `nullable=True/False` - может ли быть NULL
- `default=значение` - значение по умолчанию
- `index=True` - создать индекс (для быстрого поиска)
- `unique=True` - уникальное значение

---

## Шаг 3: Создание миграции Alembic

### 3.1. Автогенерация миграции

```bash
alembic revision --autogenerate -m "Add user_email to review_tasks"
```

Это создаст файл миграции в `alembic/versions/` с именем типа `xxxx_add_user_email_to_review_tasks.py`

### 3.2. Проверка сгенерированной миграции

Откройте созданный файл миграции и проверьте его содержимое:

```python
"""Add user_email to review_tasks

Revision ID: xxxxx
Revises: yyyyy
Create Date: 2025-12-07 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'xxxxx'
down_revision = 'yyyyy'
branch_labels = None
depends_on = None

def upgrade():
    # Добавление колонки
    op.add_column('review_tasks', 
        sa.Column('user_email', sa.String(length=255), nullable=True)
    )
    # Создание индекса (если указали index=True)
    op.create_index('ix_review_tasks_user_email', 'review_tasks', ['user_email'])

def downgrade():
    # Удаление индекса
    op.drop_index('ix_review_tasks_user_email', table_name='review_tasks')
    # Удаление колонки
    op.drop_column('review_tasks', 'user_email')
```

**Важно**: 
- Проверьте, что миграция корректна
- При необходимости отредактируйте вручную
- Убедитесь, что `downgrade()` правильно откатывает изменения

### 3.3. Ручное создание миграции (если автогенерация не работает)

Если автогенерация не сработала, создайте миграцию вручную:

```bash
alembic revision -m "Add user_email to review_tasks"
```

Затем отредактируйте созданный файл:

```python
def upgrade():
    op.add_column('review_tasks', 
        sa.Column('user_email', sa.String(length=255), nullable=True)
    )
    op.create_index('ix_review_tasks_user_email', 'review_tasks', ['user_email'])

def downgrade():
    op.drop_index('ix_review_tasks_user_email', table_name='review_tasks')
    op.drop_column('review_tasks', 'user_email')
```

---

## Шаг 4: Применение миграции

### 4.1. Проверка текущего состояния

```bash
alembic current
```

### 4.2. Просмотр истории миграций

```bash
alembic history
```

### 4.3. Применение миграции

```bash
alembic upgrade head
```

Это применит все непримененные миграции до последней версии.

### 4.4. Проверка результата

Подключитесь к БД и проверьте:

```sql
-- PostgreSQL
\c docreview
\d review_tasks
```

Или через Python:

```python
from src.db.session import SessionLocal
from src.db.models import ReviewTaskDB

db = SessionLocal()
task = db.query(ReviewTaskDB).first()
print(task.user_email)  # Должно работать
```

---

## Шаг 5: Обновление кода приложения

### 5.1. Обновление API endpoints

В `src/api/main.py` обновите endpoint для создания задачи:

```python
@app.post("/api/v1/review/start")
async def start_review(
    request: ReviewRequest,
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """Запуск анализа документации"""
    
    # Создаем задачу
    task = ReviewTask(
        document=request.document,
        document_type=request.document_type,
        context=request.context or {},
        user_email=request.user_email  # НОВОЕ ПОЛЕ
    )
    
    # Сохраняем в БД
    db_task = ReviewTaskDB(
        id=task.id,
        document=task.document,
        document_type=task.document_type,
        context=task.context,
        status=task.status.value,
        user_email=task.user_email  # НОВОЕ ПОЛЕ
    )
    
    db = SessionLocal()
    try:
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
    finally:
        db.close()
    
    # ... остальной код
```

### 5.2. Обновление Pydantic схемы запроса

```python
class ReviewRequest(BaseModel):
    """Запрос на анализ"""
    document: str
    document_type: str = "markdown"
    context: Optional[Dict[str, Any]] = None
    user_email: Optional[str] = None  # НОВОЕ ПОЛЕ
```

### 5.3. Обновление запросов к БД

Если нужно фильтровать по новому полю:

```python
from src.db.session import SessionLocal
from src.db.models import ReviewTaskDB

db = SessionLocal()
try:
    # Поиск задач по email
    tasks = db.query(ReviewTaskDB).filter(
        ReviewTaskDB.user_email == "user@example.com"
    ).all()
finally:
    db.close()
```

---

## Шаг 6: Тестирование

### 6.1. Создание теста

Создайте файл `tests/test_user_email.py`:

```python
import pytest
from src.db.models import ReviewTaskDB
from src.db.session import SessionLocal
from src.models import ReviewTask

def test_user_email_field():
    """Тест добавления user_email"""
    db = SessionLocal()
    try:
        # Создаем задачу с email
        task = ReviewTaskDB(
            document="# Test",
            user_email="test@example.com"
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        
        # Проверяем, что поле сохранено
        assert task.user_email == "test@example.com"
        
        # Проверяем поиск по email
        found = db.query(ReviewTaskDB).filter(
            ReviewTaskDB.user_email == "test@example.com"
        ).first()
        assert found is not None
        assert found.id == task.id
        
    finally:
        db.rollback()
        db.close()
```

### 6.2. Запуск теста

```bash
pytest tests/test_user_email.py -v
```

---

## Шаг 7: Откат миграции (если нужно)

Если нужно откатить миграцию:

```bash
# Откатить одну миграцию
alembic downgrade -1

# Откатить до конкретной ревизии
alembic downgrade <revision_id>

# Откатить все миграции
alembic downgrade base
```

---

## Пример: Полный цикл добавления поля

### Пример 1: Добавление поля `processing_time` (время обработки)

**1. Pydantic модель** (`src/models.py`):

```python
class ReviewTask(BaseModel):
    # ... существующие поля
    processing_time: Optional[int] = None  # Время обработки в секундах
```

**2. SQLAlchemy модель** (`src/db/models.py`):

```python
class ReviewTaskDB(Base):
    # ... существующие поля
    processing_time = Column(Integer, nullable=True)
```

**3. Миграция**:

```bash
alembic revision --autogenerate -m "Add processing_time to review_tasks"
```

**4. Применение**:

```bash
alembic upgrade head
```

**5. Использование в коде**:

```python
# В process_review функции
start_time = time.time()
# ... обработка ...
end_time = time.time()
processing_time = int(end_time - start_time)

task.processing_time = processing_time
db_task.processing_time = processing_time
db.commit()
```

---

## Пример 2: Добавление поля `tags` (список тегов)

**1. Pydantic модель**:

```python
class ReviewTask(BaseModel):
    # ... существующие поля
    tags: List[str] = Field(default_factory=list)  # Теги для категоризации
```

**2. SQLAlchemy модель**:

```python
class ReviewTaskDB(Base):
    # ... существующие поля
    tags = Column(JSON, default=list)  # Храним как JSON массив
```

**3. Миграция**:

```bash
alembic revision --autogenerate -m "Add tags to review_tasks"
```

**4. Использование**:

```python
task = ReviewTask(tags=["security", "performance"])
db_task = ReviewTaskDB(tags=["security", "performance"])
```

---

## Частые проблемы и решения

### Проблема 1: Миграция не видит изменения

**Решение**: Убедитесь, что:
- SQLAlchemy модель импортирована в `alembic/env.py`
- Модель наследуется от `Base`
- Таблица указана в `__tablename__`

### Проблема 2: Ошибка при применении миграции

**Решение**:
- Проверьте синтаксис SQL в миграции
- Убедитесь, что БД доступна
- Проверьте права доступа пользователя БД

### Проблема 3: Поле не появляется в БД

**Решение**:
- Проверьте, что миграция применена: `alembic current`
- Проверьте содержимое миграции
- Убедитесь, что используете правильную БД

### Проблема 4: Конфликт миграций

**Решение**:
- Синхронизируйте миграции с командой
- Используйте `alembic merge` для объединения веток
- При необходимости создайте новую миграцию вручную

---

## Best Practices

1. **Всегда создавайте миграции для изменений схемы БД**
2. **Проверяйте сгенерированные миграции перед применением**
3. **Тестируйте миграции на тестовой БД перед продакшеном**
4. **Используйте транзакции для отката при ошибках**
5. **Документируйте изменения в миграциях**
6. **Делайте резервные копии перед применением миграций в продакшене**

---

## Полезные команды Alembic

```bash
# Просмотр текущей версии
alembic current

# Просмотр истории
alembic history

# Просмотр SQL без применения
alembic upgrade head --sql

# Откат с просмотром SQL
alembic downgrade -1 --sql

# Создание пустой миграции
alembic revision -m "Description"

# Автогенерация миграции
alembic revision --autogenerate -m "Description"

# Применение до конкретной версии
alembic upgrade <revision_id>

# Откат до конкретной версии
alembic downgrade <revision_id>
```

---

## Дополнительные ресурсы

- [SQLAlchemy документация](https://docs.sqlalchemy.org/)
- [Alembic документация](https://alembic.sqlalchemy.org/)
- [PostgreSQL документация](https://www.postgresql.org/docs/)

