"""SQLAlchemy модели для базы данных"""
from sqlalchemy import Column, String, DateTime, Text, JSON, Integer, Float, Boolean, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from src.db.base import Base


class ReviewTaskDB(Base):
    """SQLAlchemy модель для ReviewTask"""
    __tablename__ = "review_tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document = Column(Text, nullable=False)
    document_type = Column(String(50), default="markdown")
    context = Column(JSON, default=dict)
    status = Column(String(20), default="pending")  # pending, in_progress, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Пример нового поля для проверки работы
    user_email = Column(String(255), nullable=True, index=True)  # Email пользователя


class IssueDB(Base):
    """SQLAlchemy модель для Issue"""
    __tablename__ = "issues"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    agent = Column(String(50), nullable=False)  # analyst, architect, devsecops, devops_sre
    priority = Column(String(20), nullable=False)  # critical, high, medium, low, info
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    location = Column(String(500), nullable=True)
    issue_metadata = Column(JSON, default=dict)  # Переименовано из metadata, т.к. metadata зарезервировано в SQLAlchemy
    created_at = Column(DateTime, default=datetime.utcnow)


class ReviewResultDB(Base):
    """SQLAlchemy модель для ReviewResult"""
    __tablename__ = "review_results"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), nullable=False, unique=True, index=True)
    status = Column(String(20), nullable=False)
    summary = Column(Text, nullable=False)
    report_markdown = Column(Text, nullable=False)
    report_json = Column(JSON, nullable=False)
    quality_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

