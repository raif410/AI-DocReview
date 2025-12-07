"""Синтезатор - интеграция результатов в отчет"""
from typing import Dict, Any, List
from src.models import (
    ReviewResult, ValidationResult, AnalysisResult, Issue, Priority, AgentType
)
from src.utils.ai_client import AIClient


class Synthesizer:
    """Синтезатор - создает финальный отчет"""
    
    def __init__(self):
        self.ai_client = AIClient()
    
    async def synthesize(
        self,
        task_id: str,
        agent_results: Dict[AgentType, AnalysisResult],
        validation_result: ValidationResult
    ) -> ReviewResult:
        """Создание финального отчета"""
        
        # Собираем все проблемы
        all_issues = []
        for result in agent_results.values():
            all_issues.extend(result.issues)
        
        # Добавляем пропущенные проблемы
        all_issues.extend(validation_result.missed_issues)
        
        # Приоритизируем
        prioritized_issues = self._prioritize_issues(all_issues)
        
        # Генерируем отчет
        report_markdown = await self._generate_markdown_report(
            prioritized_issues, agent_results, validation_result
        )
        
        report_json = self._generate_json_report(
            prioritized_issues, agent_results, validation_result
        )
        
        # Создаем summary
        summary = self._create_summary(prioritized_issues, validation_result)
        
        return ReviewResult(
            task_id=task_id,
            status="completed",
            issues=prioritized_issues,
            summary=summary,
            report_markdown=report_markdown,
            report_json=report_json,
            validation_result=validation_result
        )
    
    def _prioritize_issues(self, issues: List[Issue]) -> List[Issue]:
        """Приоритизация проблем"""
        priority_order = {
            Priority.CRITICAL: 0,
            Priority.HIGH: 1,
            Priority.MEDIUM: 2,
            Priority.LOW: 3,
            Priority.INFO: 4
        }
        
        return sorted(
            issues,
            key=lambda x: priority_order.get(x.priority, 5)
        )
    
    async def _generate_markdown_report(
        self,
        issues: List[Issue],
        agent_results: Dict[AgentType, AnalysisResult],
        validation_result: ValidationResult
    ) -> str:
        """Генерация Markdown отчета"""
        
        report = f"""# Отчет анализа документации

## Executive Summary

{validation_result.recommendations[0] if validation_result.recommendations else "Анализ завершен"}

**Оценка качества**: {validation_result.quality_score:.2%}
**Всего проблем**: {len(issues)}
**Критических**: {len([i for i in issues if i.priority == Priority.CRITICAL])}

## Выявленные проблемы

"""
        
        # Группируем по приоритетам
        by_priority = {}
        for issue in issues:
            if issue.priority not in by_priority:
                by_priority[issue.priority] = []
            by_priority[issue.priority].append(issue)
        
        for priority in [Priority.CRITICAL, Priority.HIGH, Priority.MEDIUM, Priority.LOW, Priority.INFO]:
            if priority in by_priority:
                report += f"\n### {priority.value.upper()}\n\n"
                for issue in by_priority[priority]:
                    report += f"#### {issue.title}\n\n"
                    report += f"**Агент**: {issue.agent.value}\n\n"
                    report += f"**Описание**: {issue.description}\n\n"
                    report += f"**Рекомендация**: {issue.recommendation}\n\n"
                    if issue.location:
                        report += f"**Местоположение**: {issue.location}\n\n"
                    report += "---\n\n"
        
        # Добавляем результаты по агентам
        report += "\n## Результаты по агентам\n\n"
        for agent, result in agent_results.items():
            report += f"### {agent.value}\n\n"
            report += f"**Статус**: {result.status.value}\n\n"
            report += f"**Найдено проблем**: {len(result.issues)}\n\n"
            report += f"**Уверенность**: {result.confidence:.2%}\n\n"
            report += f"**Резюме**: {result.summary}\n\n"
        
        return report
    
    def _generate_json_report(
        self,
        issues: List[Issue],
        agent_results: Dict[AgentType, AnalysisResult],
        validation_result: ValidationResult
    ) -> Dict[str, Any]:
        """Генерация JSON отчета"""
        return {
            "summary": {
                "total_issues": len(issues),
                "critical": len([i for i in issues if i.priority == Priority.CRITICAL]),
                "high": len([i for i in issues if i.priority == Priority.HIGH]),
                "medium": len([i for i in issues if i.priority == Priority.MEDIUM]),
                "low": len([i for i in issues if i.priority == Priority.LOW]),
                "quality_score": validation_result.quality_score
            },
            "issues": [
                {
                    "id": str(issue.id),
                    "agent": issue.agent.value,
                    "priority": issue.priority.value,
                    "title": issue.title,
                    "description": issue.description,
                    "recommendation": issue.recommendation,
                    "category": issue.category,
                    "location": issue.location
                }
                for issue in issues
            ],
            "agent_results": {
                agent.value: {
                    "status": result.status.value,
                    "issues_count": len(result.issues),
                    "confidence": result.confidence,
                    "summary": result.summary
                }
                for agent, result in agent_results.items()
            },
            "validation": {
                "is_valid": validation_result.is_valid,
                "quality_score": validation_result.quality_score,
                "missed_issues_count": len(validation_result.missed_issues),
                "conflicts_count": len(validation_result.conflicts),
                "recommendations": validation_result.recommendations
            }
        }
    
    def _create_summary(
        self,
        issues: List[Issue],
        validation_result: ValidationResult
    ) -> str:
        """Создание краткого резюме"""
        critical_count = len([i for i in issues if i.priority == Priority.CRITICAL])
        high_count = len([i for i in issues if i.priority == Priority.HIGH])
        
        summary = f"Найдено {len(issues)} проблем: {critical_count} критических, {high_count} высокого приоритета. "
        summary += f"Оценка качества анализа: {validation_result.quality_score:.2%}."
        
        if critical_count > 0:
            summary += " Требуется немедленное внимание к критическим проблемам."
        
        return summary

