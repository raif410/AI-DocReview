"""Системный аналитик - анализ требований и процессов"""
from typing import Dict, Any
from src.models import ReviewTask, AnalysisResult, AgentType, TaskStatus, Issue, Priority
from src.agents.base_agent import BaseAgent


class AnalystAgent(BaseAgent):
    """Агент-системный аналитик"""
    
    def __init__(self):
        super().__init__(AgentType.ANALYST)
    
    async def analyze(self, task: ReviewTask, context: Dict[str, Any] = None) -> AnalysisResult:
        """Анализ требований и процессов в документации"""
        
        system_prompt = """Ты опытный системный аналитик. Твоя задача - анализировать техническую документацию 
        и выявлять проблемы в требованиях, бизнес-процессах и функциональности. 
        Ищи неполные требования, противоречия, отсутствующие нефункциональные требования, 
        проблемы в логике процессов."""
        
        prompt = f"""
        Проанализируй следующую документацию как системный аналитик:
        
        {task.document}
        
        Контекст: {context or {}}
        
        Выяви проблемы в:
        1. Требованиях (полнота, корректность, согласованность)
        2. Бизнес-процессах (логика, последовательность)
        3. Функциональных требованиях
        4. Описании процессов
        
        Для каждой проблемы укажи:
        - Название проблемы
        - Описание
        - Рекомендацию по исправлению
        - Приоритет (critical, high, medium, low)
        - Категорию
        """
        
        analysis_text = await self.ai_client.analyze(prompt, system_prompt)
        
        # Парсим результат и создаем проблемы
        issues = self._parse_analysis(analysis_text, task.document)
        
        return AnalysisResult(
            agent=self.agent_type,
            status=TaskStatus.COMPLETED,
            issues=issues,
            summary=f"Найдено {len(issues)} проблем в требованиях и процессах",
            confidence=0.85
        )
    
    def _parse_analysis(self, analysis_text: str, document: str) -> list[Issue]:
        """Парсинг результата анализа"""
        issues = []
        
        # Упрощенный парсинг - в реальной версии использовался бы более сложный алгоритм
        # Проверяем типичные проблемы
        
        # Проверка на отсутствие требований
        if "требования" not in document.lower() and "requirements" not in document.lower():
            issues.append(Issue(
                agent=self.agent_type,
                priority=Priority.HIGH,
                title="Отсутствует раздел с требованиями",
                description="В документации не обнаружен явный раздел с требованиями к системе",
                recommendation="Добавить раздел с функциональными и нефункциональными требованиями",
                category="requirements"
            ))
        
        # Проверка на противоречия
        if "противоречие" in analysis_text.lower() or "contradiction" in analysis_text.lower():
            issues.append(Issue(
                agent=self.agent_type,
                priority=Priority.MEDIUM,
                title="Обнаружены возможные противоречия",
                description="В документации могут быть противоречивые требования",
                recommendation="Провести ревью требований на предмет противоречий",
                category="consistency"
            ))
        
        # Если не найдено проблем, создаем информационную
        if not issues:
            issues.append(Issue(
                agent=self.agent_type,
                priority=Priority.INFO,
                title="Требования в целом корректны",
                description="Не обнаружено критических проблем в требованиях",
                recommendation="Рекомендуется провести дополнительную проверку с экспертами",
                category="general"
            ))
        
        return issues

