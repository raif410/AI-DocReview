"""Директор - анализ задачи, стратегия, управление агентами"""
import asyncio
from typing import List, Dict, Any
from uuid import UUID
from src.models import (
    ReviewTask, Strategy, AgentType, TaskStatus, AnalysisResult
)
from src.utils.ai_client import AIClient


class Director:
    """Директор - управляет процессом анализа"""
    
    def __init__(self):
        self.ai_client = AIClient()
        self.available_agents = [
            AgentType.ANALYST,
            AgentType.ARCHITECT,
            AgentType.DEVSECOPS,
            AgentType.DEVOPS_SRE
        ]
    
    async def analyze_task(self, task: ReviewTask) -> Dict[str, Any]:
        """Анализ входящей задачи"""
        prompt = f"""
        Проанализируй задачу на анализ документации:
        
        Документ (первые 500 символов):
        {task.document[:500]}...
        
        Контекст: {task.context}
        
        Определи:
        1. Тип документации
        2. Основные области для анализа
        3. Сложность задачи
        4. Приоритетные аспекты
        """
        
        analysis = await self.ai_client.analyze(
            prompt,
            system_prompt="Ты опытный системный аналитик. Анализируй задачи на анализ документации."
        )
        
        return {
            "document_type": self._extract_document_type(task.document),
            "complexity": "medium",
            "focus_areas": self._extract_focus_areas(analysis),
            "analysis": analysis
        }
    
    async def create_strategy(self, task: ReviewTask, task_analysis: Dict[str, Any]) -> Strategy:
        """Создание стратегии анализа"""
        # Определяем какие агенты использовать
        agents_to_use = self._select_agents(task_analysis)
        
        # Определяем глубину анализа
        analysis_depth = self._determine_depth(task_analysis)
        
        # Оцениваем время
        estimated_time = len(agents_to_use) * 60  # ~60 сек на агента
        
        return Strategy(
            task_id=task.id,
            agents_to_use=agents_to_use,
            analysis_depth=analysis_depth,
            focus_areas=task_analysis.get("focus_areas", []),
            estimated_time=estimated_time
        )
    
    def _extract_document_type(self, document: str) -> str:
        """Определение типа документа"""
        document_lower = document.lower()
        if "api" in document_lower or "endpoint" in document_lower:
            return "api"
        elif "архитектура" in document_lower or "architecture" in document_lower:
            return "architecture"
        elif "безопасность" in document_lower or "security" in document_lower:
            return "security"
        else:
            return "general"
    
    def _extract_focus_areas(self, analysis: str) -> List[str]:
        """Извлечение областей фокуса из анализа"""
        # Упрощенная реализация
        areas = []
        analysis_lower = analysis.lower()
        if "требования" in analysis_lower or "requirements" in analysis_lower:
            areas.append("requirements")
        if "безопасность" in analysis_lower or "security" in analysis_lower:
            areas.append("security")
        if "производительность" in analysis_lower or "performance" in analysis_lower:
            areas.append("performance")
        if "надежность" in analysis_lower or "reliability" in analysis_lower:
            areas.append("reliability")
        return areas if areas else ["general"]
    
    def _select_agents(self, task_analysis: Dict[str, Any]) -> List[AgentType]:
        """Выбор агентов для задачи"""
        # По умолчанию используем всех агентов
        # В реальной реализации здесь была бы логика выбора
        return self.available_agents
    
    def _determine_depth(self, task_analysis: Dict[str, Any]) -> str:
        """Определение глубины анализа"""
        complexity = task_analysis.get("complexity", "medium")
        if complexity == "high":
            return "deep"
        elif complexity == "low":
            return "quick"
        else:
            return "standard"
    
    async def coordinate_agents(
        self,
        strategy: Strategy,
        task: ReviewTask,
        agent_results: Dict[AgentType, AnalysisResult]
    ) -> Dict[str, Any]:
        """Координация работы агентов"""
        # Проверяем статус всех агентов
        all_completed = all(
            result.status == TaskStatus.COMPLETED
            for result in agent_results.values()
        )
        
        if not all_completed:
            return {
                "status": "in_progress",
                "completed_agents": [
                    agent.value for agent, result in agent_results.items()
                    if result.status == TaskStatus.COMPLETED
                ]
            }
        
        # Собираем все результаты
        all_issues = []
        for result in agent_results.values():
            all_issues.extend(result.issues)
        
        return {
            "status": "completed",
            "all_issues": all_issues,
            "agent_results": agent_results
        }

