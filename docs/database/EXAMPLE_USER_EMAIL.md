# Пример: Добавление поля `user_email` в таблицу `review_tasks`

Этот документ содержит полный пример добавления нового поля `user_email` для проверки работы с БД.

---

## Шаг 1: Обновление Pydantic модели

**Файл**: `src/models.py`

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

---

## Шаг 2: Обновление SQLAlchemy модели

**Файл**: `src/db/models.py`

```python
class ReviewTaskDB(Base):
    """SQLAlchemy модель для ReviewTask"""
    __tablename__ = "review_tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document = Column(Text, nullable=False)
    document_type = Column(String(50), default="markdown")
    context = Column(JSON, default=dict)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # НОВОЕ ПОЛЕ
    user_email = Column(String(255), nullable=True, index=True)
```

---

## Шаг 3: Создание миграции

```bash
# Автогенерация миграции
alembic revision --autogenerate -m "Add user_email to review_tasks"
```

Это создаст файл в `alembic/versions/` с содержимым:

```python
"""Add user_email to review_tasks

Revision ID: xxxxx
Revises: yyyyy
Create Date: 2025-12-07 10:00:00
"""
from alembic import op
import sqlalchemy as sa

revision = 'xxxxx'
down_revision = 'yyyyy'
branch_labels = None
depends_on = None

def upgrade():
    # Добавление колонки
    op.add_column('review_tasks', 
        sa.Column('user_email', sa.String(length=255), nullable=True)
    )
    # Создание индекса
    op.create_index('ix_review_tasks_user_email', 'review_tasks', ['user_email'])

def downgrade():
    # Удаление индекса
    op.drop_index('ix_review_tasks_user_email', table_name='review_tasks')
    # Удаление колонки
    op.drop_column('review_tasks', 'user_email')
```

---

## Шаг 4: Применение миграции

```bash
# Применить миграцию
alembic upgrade head
```

Вывод должен быть примерно таким:

```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade yyyyy -> xxxxx, Add user_email to review_tasks
```

---

## Шаг 5: Проверка в БД

### Через psql:

```bash
psql -U postgres -d docreview
```

```sql
-- Проверка структуры таблицы
\d review_tasks

-- Проверка данных
SELECT id, user_email, created_at FROM review_tasks LIMIT 5;

-- Проверка индекса
\di review_tasks
```

### Через Python:

```python
from src.db.session import SessionLocal
from src.db.models import ReviewTaskDB

db = SessionLocal()
try:
    # Проверяем структуру
    task = db.query(ReviewTaskDB).first()
    if task:
        print(f"Task ID: {task.id}")
        print(f"User Email: {task.user_email}")  # Должно работать
    
    # Создаем тестовую запись
    new_task = ReviewTaskDB(
        document="# Test document",
        user_email="test@example.com"
    )
    db.add(new_task)
    db.commit()
    print("Test task created with user_email")
    
finally:
    db.close()
```

---

## Шаг 6: Обновление API

**Файл**: `src/api/main.py`

```python
class ReviewRequest(BaseModel):
    """Запрос на анализ"""
    document: str
    document_type: str = "markdown"
    context: Optional[Dict[str, Any]] = None
    user_email: Optional[str] = None  # НОВОЕ ПОЛЕ

@app.post("/api/v1/review/start")
async def start_review(
    request: ReviewRequest,
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """Запуск анализа документации"""
    
    # Создаем Pydantic модель
    task = ReviewTask(
        document=request.document,
        document_type=request.document_type,
        context=request.context or {},
        user_email=request.user_email  # НОВОЕ ПОЛЕ
    )
    
    # Сохраняем в БД
    from src.db.session import SessionLocal
    from src.db.models import ReviewTaskDB
    
    db = SessionLocal()
    try:
        db_task = ReviewTaskDB(
            id=task.id,
            document=task.document,
            document_type=task.document_type,
            context=task.context,
            status=task.status.value,
            user_email=task.user_email  # НОВОЕ ПОЛЕ
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
    finally:
        db.close()
    
    tasks_storage[task.id] = task
    
    # ... остальной код
```

---

## Шаг 7: Тестирование

### Тест через API:

```bash
curl -X POST "http://localhost:8000/api/v1/review/start" \
  -H "Content-Type: application/json" \
  -d '{
    "document": "# Test Document",
    "user_email": "test@example.com"
  }'
```

### Тест через Python:

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/review/start",
    json={
        "document": "# Test Document",
        "user_email": "test@example.com"
    }
)

print(response.json())
```

### Проверка в БД:

```python
from src.db.session import SessionLocal
from src.db.models import ReviewTaskDB

db = SessionLocal()
try:
    # Ищем задачу по email
    task = db.query(ReviewTaskDB).filter(
        ReviewTaskDB.user_email == "test@example.com"
    ).first()
    
    if task:
        print(f"Found task: {task.id}")
        print(f"Email: {task.user_email}")
        print(f"Document: {task.document[:50]}...")
    else:
        print("Task not found")
finally:
    db.close()
```

---

## Шаг 8: Откат (если нужно)

Если нужно откатить миграцию:

```bash
alembic downgrade -1
```

Это выполнит функцию `downgrade()` из миграции и удалит поле.

---

## Проверочный чеклист

- [ ] Pydantic модель обновлена
- [ ] SQLAlchemy модель обновлена
- [ ] Миграция создана
- [ ] Миграция применена (`alembic upgrade head`)
- [ ] Поле появилось в БД (проверено через `\d review_tasks`)
- [ ] API обновлен для работы с новым полем
- [ ] Тесты проходят
- [ ] Документация обновлена

---

## Частые ошибки

### Ошибка: "Table 'review_tasks' does not exist"

**Решение**: Сначала создайте таблицы:

```bash
# Создать первую миграцию
alembic revision --autogenerate -m "Initial migration"

# Применить
alembic upgrade head
```

### Ошибка: "Column 'user_email' already exists"

**Решение**: Поле уже существует. Проверьте текущее состояние:

```bash
alembic current
```

### Ошибка: "Could not determine revision"

**Решение**: Инициализируйте Alembic:

```bash
alembic init alembic
```

Затем обновите `alembic/env.py` как показано в документации.

---

## Готово!

Теперь поле `user_email` добавлено и готово к использованию. Вы можете:

1. Сохранять email при создании задач
2. Фильтровать задачи по email
3. Использовать email в отчетах

