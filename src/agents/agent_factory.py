"""Фабрика для создания агентов"""
from src.models import AgentType
from .analyst.analyst import AnalystAgent
from .architect.architect import ArchitectAgent
from .devsecops.devsecops import DevSecOpsAgent
from .devops_sre.devops_sre import DevOpsSREAgent


class AgentFactory:
    """Фабрика для создания агентов"""
    
    _agents = {
        AgentType.ANALYST: AnalystAgent,
        AgentType.ARCHITECT: ArchitectAgent,
        AgentType.DEVSECOPS: DevSecOpsAgent,
        AgentType.DEVOPS_SRE: DevOpsSREAgent
    }
    
    @classmethod
    def create_agent(cls, agent_type: AgentType):
        """Создать агента по типу"""
        agent_class = cls._agents.get(agent_type)
        if not agent_class:
            raise ValueError(f"Неизвестный тип агента: {agent_type}")
        return agent_class()

