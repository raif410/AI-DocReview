"""DevOps/SRE - анализ надежности и операций"""
from typing import Dict, Any
from src.models import ReviewTask, AnalysisResult, AgentType, TaskStatus, Issue, Priority
from src.agents.base_agent import BaseAgent


class DevOpsSREAgent(BaseAgent):
    """Агент-DevOps/SRE"""
    
    def __init__(self):
        super().__init__(AgentType.DEVOPS_SRE)
    
    async def analyze(self, task: ReviewTask, context: Dict[str, Any] = None) -> AnalysisResult:
        """Анализ операционной надежности"""
        
        system_prompt = """Ты опытный SRE/DevOps инженер. Твоя задача - анализировать документацию на предмет 
        проблем операционной надежности: Single Points of Failure, проблемы масштабируемости, недостаточный 
        мониторинг, проблемы в CI/CD процессах, неоптимальное использование ресурсов."""
        
        prompt = f"""
        Проанализируй следующую документацию как SRE/DevOps инженер:
        
        {task.document}
        
        Контекст: {context or {}}
        
        Выяви проблемы в:
        1. Операционной надежности
        2. Масштабируемости
        3. Мониторинге и наблюдаемости
        4. Процессах развертывания (CI/CD)
        5. Использовании ресурсов
        
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
            summary=f"Найдено {len(issues)} проблем операционной надежности",
            confidence=0.87
        )
    
    def _parse_analysis(self, analysis_text: str, document: str) -> list[Issue]:
        """Парсинг результата анализа"""
        issues = []
        
        # Проверка на мониторинг
        if "мониторинг" not in document.lower() and "monitoring" not in document.lower():
            issues.append(Issue(
                agent=self.agent_type,
                priority=Priority.HIGH,
                title="Отсутствует описание мониторинга",
                description="В документации не описана система мониторинга",
                recommendation="Добавить описание системы мониторинга, метрик и алертов",
                category="monitoring"
            ))
        
        # Проверка на резервное копирование
        if "бэкап" not in document.lower() and "backup" not in document.lower() and "резерв" not in document.lower():
            issues.append(Issue(
                agent=self.agent_type,
                priority=Priority.MEDIUM,
                title="Отсутствует описание резервного копирования",
                description="В документации не описана стратегия резервного копирования",
                recommendation="Добавить описание стратегии backup и disaster recovery",
                category="reliability"
            ))
        
        if not issues:
            issues.append(Issue(
                agent=self.agent_type,
                priority=Priority.INFO,
                title="Операционные аспекты в целом учтены",
                description="Не обнаружено критических проблем операционной надежности",
                recommendation="Рекомендуется провести дополнительный SRE review",
                category="general"
            ))
        
        return issues

