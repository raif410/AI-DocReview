"""Скрипт для тестирования добавления нового поля в БД"""
from src.db.session import SessionLocal
from src.db.models import ReviewTaskDB
from datetime import datetime
import uuid

def test_user_email_field():
    """Тест работы с полем user_email"""
    print("Testing user_email field...")
    
    db = SessionLocal()
    try:
        # 1. Создаем задачу с email
        print("\n1. Creating task with user_email...")
        task = ReviewTaskDB(
            id=uuid.uuid4(),
            document="# Test Document\n\nThis is a test.",
            document_type="markdown",
            status="pending",
            user_email="test@example.com"  # НОВОЕ ПОЛЕ
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        
        print(f"✅ Task created: {task.id}")
        print(f"   Email: {task.user_email}")
        
        # 2. Проверяем чтение
        print("\n2. Reading task from database...")
        found_task = db.query(ReviewTaskDB).filter(
            ReviewTaskDB.id == task.id
        ).first()
        
        if found_task and found_task.user_email == "test@example.com":
            print(f"✅ Task found: {found_task.id}")
            print(f"   Email: {found_task.user_email}")
        else:
            print("❌ Task not found or email mismatch")
        
        # 3. Тестируем поиск по email
        print("\n3. Searching tasks by email...")
        tasks_by_email = db.query(ReviewTaskDB).filter(
            ReviewTaskDB.user_email == "test@example.com"
        ).all()
        
        print(f"✅ Found {len(tasks_by_email)} task(s) with email test@example.com")
        
        # 4. Обновляем email
        print("\n4. Updating email...")
        task.user_email = "updated@example.com"
        db.commit()
        db.refresh(task)
        
        print(f"✅ Email updated: {task.user_email}")
        
        # 5. Проверяем NULL значение
        print("\n5. Testing NULL email...")
        task2 = ReviewTaskDB(
            id=uuid.uuid4(),
            document="# Another Test",
            user_email=None  # NULL значение
        )
        db.add(task2)
        db.commit()
        db.refresh(task2)
        
        print(f"✅ Task with NULL email created: {task2.id}")
        print(f"   Email: {task2.user_email}")
        
        # Очистка тестовых данных
        print("\n6. Cleaning up test data...")
        db.delete(task)
        db.delete(task2)
        db.commit()
        print("✅ Test data cleaned up")
        
        print("\n" + "="*50)
        print("✅ ALL TESTS PASSED!")
        print("="*50)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_user_email_field()

