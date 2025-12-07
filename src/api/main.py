"""FastAPI приложение"""
import asyncio
import logging
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
from uuid import UUID
from pydantic import BaseModel
from src.config import settings
from src.models import ReviewTask, ReviewResult, TaskStatus
from src.core.director import Director
from src.core.critic import Critic
from src.core.synthesizer import Synthesizer
from src.agents.agent_factory import AgentFactory
from src.models import AgentType

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    debug=settings.debug
)

# Инициализация компонентов (ленивая инициализация)
director = None
critic = None
synthesizer = None

def get_director():
    """Ленивая инициализация директора"""
    global director
    if director is None:
        director = Director()
    return director

def get_critic():
    """Ленивая инициализация критика"""
    global critic
    if critic is None:
        critic = Critic()
    return critic

def get_synthesizer():
    """Ленивая инициализация синтезатора"""
    global synthesizer
    if synthesizer is None:
        synthesizer = Synthesizer()
    return synthesizer

# Хранилище задач (в продакшене использовалась бы БД)
tasks_storage: Dict[UUID, ReviewTask] = {}
results_storage: Dict[UUID, ReviewResult] = {}


@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "message": "DocReview AI API",
        "version": settings.api_version
    }


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}


class ReviewRequest(BaseModel):
    """Запрос на анализ"""
    document: str
    document_type: str = "markdown"
    context: Optional[Dict[str, Any]] = None


@app.post("/api/v1/review/start")
async def start_review(
    request: ReviewRequest,
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """Запуск анализа документации"""
    
    # Создаем задачу
    task = ReviewTask(
        document=request.document,
        document_type=request.document_type,
        context=request.context or {}
    )
    tasks_storage[task.id] = task
    
    # Запускаем анализ в фоне
    if background_tasks:
        background_tasks.add_task(process_review, task.id)
    
    return {
        "task_id": str(task.id),
        "status": "started",
        "estimated_time": 180  # ~3 минуты
    }


@app.get("/api/v1/review/{task_id}/status")
async def get_review_status(task_id: UUID) -> Dict[str, Any]:
    """Получение статуса анализа"""
    
    task = tasks_storage.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    result = results_storage.get(task_id)
    
    return {
        "task_id": str(task_id),
        "status": task.status.value,
        "has_result": result is not None
    }


@app.get("/api/v1/review/{task_id}/results")
async def get_review_results(task_id: UUID) -> Dict[str, Any]:
    """Получение результатов анализа"""
    
    result = results_storage.get(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Результаты не найдены")
    
    return {
        "task_id": str(task_id),
        "status": result.status.value,
        "summary": result.summary,
        "issues_count": len(result.issues),
        "quality_score": result.validation_result.quality_score if result.validation_result else None,
        "report_json": result.report_json
    }


@app.get("/api/v1/review/{task_id}/report")
async def get_review_report(task_id: UUID, format: str = "markdown") -> Dict[str, Any]:
    """Получение отчета"""
    
    result = results_storage.get(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Результаты не найдены")
    
    if format == "markdown":
        return {
            "task_id": str(task_id),
            "format": "markdown",
            "report": result.report_markdown
        }
    elif format == "json":
        return {
            "task_id": str(task_id),
            "format": "json",
            "report": result.report_json
        }
    else:
        raise HTTPException(status_code=400, detail="Неподдерживаемый формат")


async def process_review(task_id: UUID):
    """Обработка анализа документации"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        task = tasks_storage[task_id]
        task.status = TaskStatus.IN_PROGRESS
        logger.info(f"Starting review for task {task_id}")
        
        # 1. Директор анализирует задачу
        director_instance = get_director()
        logger.info("Director initialized, analyzing task...")
        task_analysis = await director_instance.analyze_task(task)
        
        # 2. Директор создает стратегию
        logger.info("Creating strategy...")
        strategy = await director_instance.create_strategy(task, task_analysis)
        
        # 3. Запускаем агентов параллельно
        logger.info(f"Starting {len(strategy.agents_to_use)} agents...")
        agent_tasks = []
        agent_results = {}
        
        for agent_type in strategy.agents_to_use:
            agent = AgentFactory.create_agent(agent_type)
            agent_tasks.append(agent.analyze(task, task.context))
        
        # Ждем результаты всех агентов
        results = await asyncio.gather(*agent_tasks)
        
        for agent_type, result in zip(strategy.agents_to_use, results):
            agent_results[agent_type] = result
        
        # 4. Критик валидирует результаты
        logger.info("Validating results with critic...")
        critic_instance = get_critic()
        validation_result = await critic_instance.validate(agent_results)
        
        # 5. Синтезатор создает финальный отчет
        logger.info("Synthesizing final report...")
        synthesizer_instance = get_synthesizer()
        review_result = await synthesizer_instance.synthesize(
            str(task_id),
            agent_results,
            validation_result
        )
        
        # Сохраняем результат
        results_storage[task_id] = review_result
        task.status = TaskStatus.COMPLETED
        logger.info(f"Review completed for task {task_id}")
        
    except Exception as e:
        logger.error(f"Error processing review {task_id}: {e}", exc_info=True)
        if task_id in tasks_storage:
            tasks_storage[task_id].status = TaskStatus.FAILED
        # Не пробрасываем исключение, чтобы не падал background task


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port
    )

