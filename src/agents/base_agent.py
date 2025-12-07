"""Базовый класс для агентов"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from src.models import ReviewTask, AnalysisResult, AgentType
from src.utils.ai_client import AIClient


class BaseAgent(ABC):
    """Базовый класс для всех агентов-специалистов"""
    
    def __init__(self, agent_type: AgentType):
        self.agent_type = agent_type
        self.ai_client = AIClient()
    
    @abstractmethod
    async def analyze(self, task: ReviewTask, context: Dict[str, Any] = None) -> AnalysisResult:
        """Выполнить анализ документации"""
        pass
    
    def _create_issue(
        self,
        title: str,
        description: str,
        recommendation: str,
        priority: str,
        category: str,
        location: str = None
    ):
        """Создать проблему (будет импортирован из models)"""
        from src.models import Issue, Priority
        return Issue(
            agent=self.agent_type,
            priority=Priority(priority),
            title=title,
            description=description,
            recommendation=recommendation,
            category=category,
            location=location
        )

