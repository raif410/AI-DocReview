"""Критик - валидация выводов, оценка рисков"""
from typing import List, Dict, Any
from src.models import (
    ValidationResult, AnalysisResult, Issue, Priority, AgentType
)
from src.utils.ai_client import AIClient


class Critic:
    """Критик - валидирует результаты анализа"""
    
    def __init__(self):
        self.ai_client = AIClient()
    
    async def validate(
        self,
        agent_results: Dict[AgentType, AnalysisResult]
    ) -> ValidationResult:
        """Валидация результатов от всех агентов"""
        
        # Собираем все проблемы
        all_issues = []
        for result in agent_results.values():
            all_issues.extend(result.issues)
        
        # Проверяем логическую корректность
        logical_errors = await self._check_logic(all_issues)
        
        # Выявляем пропущенные проблемы
        missed_issues = await self._detect_missed_issues(agent_results)
        
        # Проверяем согласованность
        conflicts = await self._check_consistency(agent_results)
        
        # Оцениваем критичность
        criticality = self._assess_criticality(all_issues)
        
        # Оцениваем качество
        quality_score = self._calculate_quality_score(
            agent_results, logical_errors, missed_issues
        )
        
        return ValidationResult(
            is_valid=len(logical_errors) == 0 and len(conflicts) == 0,
            quality_score=quality_score,
            missed_issues=missed_issues,
            conflicts=conflicts,
            criticality_assessment=criticality,
            recommendations=self._generate_recommendations(
                logical_errors, missed_issues, conflicts
            )
        )
    
    async def _check_logic(self, issues: List[Issue]) -> List[str]:
        """Проверка логической корректности"""
        errors = []
        
        # Проверяем на дубликаты
        seen_titles = set()
        for issue in issues:
            if issue.title in seen_titles:
                errors.append(f"Дубликат проблемы: {issue.title}")
            seen_titles.add(issue.title)
        
        # Проверяем на противоречия в приоритетах
        # (упрощенная проверка)
        
        return errors
    
    async def _detect_missed_issues(
        self,
        agent_results: Dict[AgentType, AnalysisResult]
    ) -> List[Issue]:
        """Выявление пропущенных проблем"""
        # Упрощенная реализация
        # В реальной версии здесь был бы AI-анализ на предмет типичных проблем
        missed = []
        
        # Проверяем наличие критических проблем безопасности
        has_security_issues = any(
            issue.priority == Priority.CRITICAL and issue.agent == AgentType.DEVSECOPS
            for result in agent_results.values()
            for issue in result.issues
        )
        
        if not has_security_issues:
            # Создаем информационную проблему
            missed.append(Issue(
                agent=AgentType.DEVSECOPS,
                priority=Priority.INFO,
                title="Рекомендуется проверить безопасность",
                description="Не обнаружено критических проблем безопасности, но рекомендуется дополнительная проверка",
                recommendation="Провести дополнительный аудит безопасности",
                category="security"
            ))
        
        return missed
    
    async def _check_consistency(
        self,
        agent_results: Dict[AgentType, AnalysisResult]
    ) -> List[str]:
        """Проверка согласованности результатов"""
        conflicts = []
        
        # Собираем все проблемы по категориям
        issues_by_category = {}
        for result in agent_results.values():
            for issue in result.issues:
                if issue.category not in issues_by_category:
                    issues_by_category[issue.category] = []
                issues_by_category[issue.category].append(issue)
        
        # Проверяем на противоречия
        # (упрощенная проверка)
        
        return conflicts
    
    def _assess_criticality(self, issues: List[Issue]) -> Dict[str, Priority]:
        """Оценка критичности проблем"""
        criticality = {}
        for issue in issues:
            criticality[issue.id.hex] = issue.priority
        return criticality
    
    def _calculate_quality_score(
        self,
        agent_results: Dict[AgentType, AnalysisResult],
        logical_errors: List[str],
        missed_issues: List[Issue]
    ) -> float:
        """Расчет оценки качества"""
        # Базовая оценка
        base_score = 0.8
        
        # Штрафы за ошибки
        if logical_errors:
            base_score -= len(logical_errors) * 0.1
        
        # Штрафы за пропущенные проблемы
        if missed_issues:
            base_score -= len(missed_issues) * 0.05
        
        # Бонусы за детальность
        total_issues = sum(len(r.issues) for r in agent_results.values())
        if total_issues > 10:
            base_score += 0.1
        
        return max(0.0, min(1.0, base_score))
    
    def _generate_recommendations(
        self,
        logical_errors: List[str],
        missed_issues: List[Issue],
        conflicts: List[str]
    ) -> List[str]:
        """Генерация рекомендаций"""
        recommendations = []
        
        if logical_errors:
            recommendations.append("Исправить логические ошибки в анализе")
        
        if missed_issues:
            recommendations.append("Провести дополнительный анализ для выявления пропущенных проблем")
        
        if conflicts:
            recommendations.append("Разрешить противоречия между результатами агентов")
        
        if not recommendations:
            recommendations.append("Анализ выполнен качественно")
        
        return recommendations

