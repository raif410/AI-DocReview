"""DevSecOps - анализ безопасности"""
from typing import Dict, Any
from src.models import ReviewTask, AnalysisResult, AgentType, TaskStatus, Issue, Priority
from src.agents.base_agent import BaseAgent


class DevSecOpsAgent(BaseAgent):
    """Агент-DevSecOps"""
    
    def __init__(self):
        super().__init__(AgentType.DEVSECOPS)
    
    async def analyze(self, task: ReviewTask, context: Dict[str, Any] = None) -> AnalysisResult:
        """Анализ безопасности"""
        
        system_prompt = """Ты опытный специалист по безопасности (DevSecOps). Твоя задача - анализировать 
        документацию на предмет проблем безопасности: уязвимости (OWASP Top 10), несоответствие стандартам 
        (ISO 27001, PCI DSS), проблемы безопасности инфраструктуры, пробелы в процессах безопасности."""
        
        prompt = f"""
        Проанализируй следующую документацию как специалист по безопасности:
        
        {task.document}
        
        Контекст: {context or {}}
        
        Выяви проблемы безопасности:
        1. Уязвимости (OWASP Top 10)
        2. Несоответствие стандартам безопасности
        3. Проблемы безопасности инфраструктуры
        4. Пробелы в процессах DevSecOps
        5. Небезопасные конфигурации
        
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
            summary=f"Найдено {len(issues)} проблем безопасности",
            confidence=0.90
        )
    
    def _parse_analysis(self, analysis_text: str, document: str) -> list[Issue]:
        """Парсинг результата анализа"""
        issues = []
        
        # Проверка на хранение паролей в открытом виде
        if "пароль" in document.lower() or "password" in document.lower():
            if "хеш" not in document.lower() and "hash" not in document.lower() and "bcrypt" not in document.lower():
                issues.append(Issue(
                    agent=self.agent_type,
                    priority=Priority.CRITICAL,
                    title="Пароли могут храниться в открытом виде",
                    description="В документации упоминаются пароли, но не указано использование хеширования",
                    recommendation="Использовать bcrypt или аналогичное хеширование для паролей",
                    category="authentication"
                ))
        
        # Проверка на HTTPS
        if "api" in document.lower() or "endpoint" in document.lower():
            if "https" not in document.lower() and "tls" not in document.lower() and "ssl" not in document.lower():
                issues.append(Issue(
                    agent=self.agent_type,
                    priority=Priority.HIGH,
                    title="Отсутствует упоминание HTTPS/TLS",
                    description="В документации описаны API endpoints, но не указано использование HTTPS",
                    recommendation="Обязательно использовать HTTPS для всех API endpoints",
                    category="encryption"
                ))
        
        if not issues:
            issues.append(Issue(
                agent=self.agent_type,
                priority=Priority.INFO,
                title="Базовые аспекты безопасности учтены",
                description="Не обнаружено критических проблем безопасности",
                recommendation="Рекомендуется провести дополнительный security audit",
                category="general"
            ))
        
        return issues

