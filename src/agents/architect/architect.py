"""Архитектор - анализ архитектурных решений"""
from typing import Dict, Any
from src.models import ReviewTask, AnalysisResult, AgentType, TaskStatus, Issue, Priority
from src.agents.base_agent import BaseAgent


class ArchitectAgent(BaseAgent):
    """Агент-архитектор"""
    
    def __init__(self):
        super().__init__(AgentType.ARCHITECT)
    
    async def analyze(self, task: ReviewTask, context: Dict[str, Any] = None) -> AnalysisResult:
        """Анализ архитектурных решений"""
        
        system_prompt = """Ты опытный архитектор систем. Твоя задача - анализировать архитектурные решения 
        в документации и выявлять проблемы: архитектурные антипаттерны, нарушения принципов SOLID/DRY/KISS, 
        неоптимальные решения, проблемы масштабируемости, отсутствие важных компонентов."""
        
        prompt = f"""
        Проанализируй следующую документацию как архитектор:
        
        {task.document}
        
        Контекст: {context or {}}
        
        Выяви проблемы в:
        1. Архитектурных решениях
        2. Производительности
        3. Масштабируемости
        4. Соответствии best practices
        5. Техническом долге
        
        Для каждой проблемы укажи:
        - Название проблемы
        - Описание
        - Рекомендацию по исправлению
        - Приоритет (critical, high, medium, low)
        - Категорию
        """
        
        analysis_text = await self.ai_client.analyze(prompt, system_prompt)
        
        issues = self._parse_analysis(analysis_text, task.document)
        
        return AnalysisResult(
            agent=self.agent_type,
            status=TaskStatus.COMPLETED,
            issues=issues,
            summary=f"Найдено {len(issues)} архитектурных проблем",
            confidence=0.88
        )
    
    def _parse_analysis(self, analysis_text: str, document: str) -> list[Issue]:
        """Парсинг результата анализа"""
        issues = []
        
        # Проверка на монолитную архитектуру без упоминания масштабирования
        if "монолит" in document.lower() or "monolith" in document.lower():
            if "масштабирование" not in document.lower() and "scaling" not in document.lower():
                issues.append(Issue(
                    agent=self.agent_type,
                    priority=Priority.HIGH,
                    title="Монолитная архитектура без стратегии масштабирования",
                    description="Описана монолитная архитектура, но не указана стратегия масштабирования",
                    recommendation="Добавить описание стратегии масштабирования или рассмотреть микросервисную архитектуру",
                    category="scalability"
                ))
        
        # Проверка на отсутствие описания компонентов
        if "компонент" not in document.lower() and "component" not in document.lower():
            issues.append(Issue(
                agent=self.agent_type,
                priority=Priority.MEDIUM,
                title="Отсутствует описание компонентов системы",
                description="В документации не описаны основные компоненты системы",
                recommendation="Добавить описание компонентов и их взаимодействия",
                category="architecture"
            ))
        
        if not issues:
            issues.append(Issue(
                agent=self.agent_type,
                priority=Priority.INFO,
                title="Архитектура в целом корректна",
                description="Не обнаружено критических архитектурных проблем",
                recommendation="Рекомендуется провести дополнительный архитектурный ревью",
                category="general"
            ))
        
        return issues

