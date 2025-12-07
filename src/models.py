"""Модели данных для DocReview AI"""
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Priority(str, Enum):
    """Приоритет проблемы"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AgentType(str, Enum):
    """Тип агента"""
    ANALYST = "analyst"
    ARCHITECT = "architect"
    DEVSECOPS = "devsecops"
    DEVOPS_SRE = "devops_sre"


class TaskStatus(str, Enum):
    """Статус задачи"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Issue(BaseModel):
    """Выявленная проблема"""
    id: UUID = Field(default_factory=uuid4)
    agent: AgentType
    priority: Priority
    title: str
    description: str
    recommendation: str
    category: str
    location: Optional[str] = None  # Где в документе найдена проблема
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AnalysisResult(BaseModel):
    """Результат анализа агента"""
    agent: AgentType
    status: TaskStatus
    issues: List[Issue] = Field(default_factory=list)
    summary: str
    confidence: float = Field(ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ValidationResult(BaseModel):
    """Результат валидации Критиком"""
    is_valid: bool
    quality_score: float = Field(ge=0.0, le=1.0)
    missed_issues: List[Issue] = Field(default_factory=list)
    conflicts: List[str] = Field(default_factory=list)
    criticality_assessment: Dict[str, Priority] = Field(default_factory=dict)
    recommendations: List[str] = Field(default_factory=list)


class ReviewTask(BaseModel):
    """Задача на анализ документации"""
    id: UUID = Field(default_factory=uuid4)
    document: str  # Содержимое документации
    document_type: str = "markdown"
    context: Dict[str, Any] = Field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ReviewResult(BaseModel):
    """Финальный результат анализа"""
    task_id: UUID
    status: TaskStatus
    issues: List[Issue] = Field(default_factory=list)
    summary: str
    report_markdown: str
    report_json: Dict[str, Any]
    validation_result: Optional[ValidationResult] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Strategy(BaseModel):
    """Стратегия анализа от Директора"""
    task_id: UUID
    agents_to_use: List[AgentType]
    analysis_depth: str = "standard"  # quick, standard, deep
    focus_areas: List[str] = Field(default_factory=list)
    estimated_time: int  # в секундах
    created_at: datetime = Field(default_factory=datetime.utcnow)

