# 🏗️ Архитектура DocReview AI

## Обзор системы

DocReview AI - это многоагентная система для анализа технической документации, состоящая из 7 компонентов: 3 ядра (Director, Critic, Synthesizer) и 4 специалиста (Analyst, Architect, DevSecOps, DevOps/SRE).

## Архитектурная диаграмма компонентов

```mermaid
graph TB
    subgraph "API Layer"
        API[FastAPI Application<br/>/api/v1/review/*]
    end
    
    subgraph "Core Components"
        DIR[Director<br/>Анализ задачи<br/>Стратегия<br/>Координация]
        CRT[Critic<br/>Валидация<br/>Оценка рисков<br/>Качество]
        SYN[Synthesizer<br/>Интеграция<br/>Отчет<br/>Приоритизация]
    end
    
    subgraph "Specialist Agents"
        ANA[Analyst Agent<br/>Системный анализ<br/>Требования<br/>Бизнес-процессы]
        ARC[Architect Agent<br/>Архитектура<br/>Производительность<br/>Масштабируемость]
        DSEC[DevSecOps Agent<br/>Безопасность<br/>Уязвимости<br/>Compliance]
        DSRE[DevOps/SRE Agent<br/>Надежность<br/>Мониторинг<br/>Операции]
    end
    
    subgraph "Infrastructure"
        AI[AI Client<br/>OpenAI/DeepSeek API]
        DB[(PostgreSQL<br/>Задачи и результаты)]
        CACHE[(Redis<br/>Кэш и очереди)]
    end
    
    API -->|1. Создание задачи| DIR
    DIR -->|2. Анализ задачи| AI
    DIR -->|3. Стратегия| DIR
    DIR -->|4. Координация| ANA
    DIR -->|4. Координация| ARC
    DIR -->|4. Координация| DSEC
    DIR -->|4. Координация| DSRE
    
    ANA -->|Результаты| CRT
    ARC -->|Результаты| CRT
    DSEC -->|Результаты| CRT
    DSRE -->|Результаты| CRT
    
    CRT -->|Валидация| SYN
    SYN -->|Финальный отчет| API
    
    DIR -.->|Сохранение| DB
    CRT -.->|Сохранение| DB
    SYN -.->|Сохранение| DB
    
    AI -.->|Кэширование| CACHE
    
    style DIR fill:#e1f5ff
    style CRT fill:#fff4e1
    style SYN fill:#e8f5e9
    style ANA fill:#f3e5f5
    style ARC fill:#f3e5f5
    style DSEC fill:#f3e5f5
    style DSRE fill:#f3e5f5
```

## Sequence диаграмма: Workflow анализа

```mermaid
sequenceDiagram
    participant Client
    participant API as FastAPI
    participant DIR as Director
    participant ANA as Analyst
    participant ARC as Architect
    participant DSEC as DevSecOps
    participant DSRE as DevOps/SRE
    participant CRT as Critic
    participant SYN as Synthesizer
    participant DB as Database
    
    Client->>API: POST /api/v1/review/start<br/>{document, context}
    API->>DB: Сохранить ReviewTask
    API-->>Client: {task_id, status: "started"}
    
    API->>DIR: analyze_task(task)
    DIR->>DIR: Анализ документа<br/>Определение типа<br/>Оценка сложности
    DIR->>DIR: create_strategy(task, analysis)
    DIR->>DB: Сохранить Strategy
    
    par Параллельный анализ
        DIR->>ANA: analyze(task, context)
        ANA->>ANA: Анализ требований<br/>Бизнес-процессы
        ANA-->>DIR: AnalysisResult
    and
        DIR->>ARC: analyze(task, context)
        ARC->>ARC: Архитектурный анализ<br/>Производительность
        ARC-->>DIR: AnalysisResult
    and
        DIR->>DSEC: analyze(task, context)
        DSEC->>DSEC: Анализ безопасности<br/>Уязвимости
        DSEC-->>DIR: AnalysisResult
    and
        DIR->>DSRE: analyze(task, context)
        DSRE->>DSRE: Операционный анализ<br/>Мониторинг
        DSRE-->>DIR: AnalysisResult
    end
    
    DIR->>CRT: validate(agent_results)
    CRT->>CRT: Проверка логики<br/>Выявление пропусков<br/>Проверка согласованности
    CRT->>CRT: Оценка критичности<br/>Оценка качества
    CRT-->>DIR: ValidationResult
    
    DIR->>SYN: synthesize(task_id, results, validation)
    SYN->>SYN: Сбор всех проблем<br/>Приоритизация<br/>Генерация отчета
    SYN->>DB: Сохранить ReviewResult
    SYN-->>DIR: ReviewResult
    
    DIR->>DB: Обновить статус задачи
    API->>Client: GET /api/v1/review/{task_id}/results
    API-->>Client: ReviewResult (Markdown/JSON)
```

## Диаграмма классов данных

```mermaid
classDiagram
    class ReviewTask {
        +UUID id
        +str document
        +str document_type
        +Dict context
        +TaskStatus status
        +datetime created_at
        +datetime updated_at
    }
    
    class Strategy {
        +UUID task_id
        +List~AgentType~ agents_to_use
        +str analysis_depth
        +List~str~ focus_areas
        +int estimated_time
        +datetime created_at
    }
    
    class AnalysisResult {
        +AgentType agent
        +TaskStatus status
        +List~Issue~ issues
        +str summary
        +float confidence
        +Dict metadata
        +datetime created_at
    }
    
    class Issue {
        +UUID id
        +AgentType agent
        +Priority priority
        +str title
        +str description
        +str recommendation
        +str category
        +str location
        +Dict metadata
    }
    
    class ValidationResult {
        +bool is_valid
        +float quality_score
        +List~Issue~ missed_issues
        +List~str~ conflicts
        +Dict criticality_assessment
        +List~str~ recommendations
    }
    
    class ReviewResult {
        +UUID task_id
        +TaskStatus status
        +List~Issue~ issues
        +str summary
        +str report_markdown
        +Dict report_json
        +ValidationResult validation_result
        +datetime created_at
    }
    
    ReviewTask --> Strategy : creates
    Strategy --> AnalysisResult : produces
    AnalysisResult --> Issue : contains
    AnalysisResult --> ValidationResult : validated_by
    ValidationResult --> ReviewResult : included_in
    ReviewResult --> Issue : contains
```

## Диаграмма состояния задачи

```mermaid
stateDiagram-v2
    [*] --> PENDING: Создание задачи
    
    PENDING --> IN_PROGRESS: Начало анализа
    IN_PROGRESS --> IN_PROGRESS: Анализ агентами
    IN_PROGRESS --> IN_PROGRESS: Валидация
    IN_PROGRESS --> IN_PROGRESS: Синтез отчета
    IN_PROGRESS --> COMPLETED: Успешное завершение
    IN_PROGRESS --> FAILED: Ошибка обработки
    
    COMPLETED --> [*]
    FAILED --> [*]
    
    note right of PENDING
        Задача создана
        Ожидает обработки
    end note
    
    note right of IN_PROGRESS
        Director анализирует
        Агенты работают
        Critic валидирует
        Synthesizer создает отчет
    end note
    
    note right of COMPLETED
        Отчет готов
        Результаты доступны
    end note
```

## Диаграмма развертывания

```mermaid
graph TB
    subgraph "Client Layer"
        WEB[Web Browser<br/>Swagger UI]
        CLI[CLI Scripts<br/>Python]
        APP[External Apps<br/>API Clients]
    end
    
    subgraph "API Gateway"
        LB[Load Balancer<br/>Nginx/Traefik]
    end
    
    subgraph "Application Layer"
        API1[FastAPI Instance 1]
        API2[FastAPI Instance 2]
        API3[FastAPI Instance N]
    end
    
    subgraph "Core Services"
        DIR_SVC[Director Service]
        CRT_SVC[Critic Service]
        SYN_SVC[Synthesizer Service]
    end
    
    subgraph "Agent Services"
        ANA_SVC[Analyst Service]
        ARC_SVC[Architect Service]
        DSEC_SVC[DevSecOps Service]
        DSRE_SVC[DevOps/SRE Service]
    end
    
    subgraph "Data Layer"
        PG[(PostgreSQL<br/>Primary)]
        PG_REPLICA[(PostgreSQL<br/>Replica)]
        REDIS[(Redis Cluster<br/>Cache & Queue)]
    end
    
    subgraph "External Services"
        OPENAI[OpenAI/DeepSeek API]
    end
    
    subgraph "Monitoring"
        PROM[Prometheus]
        GRAF[Grafana]
        ELK[ELK Stack]
    end
    
    WEB --> LB
    CLI --> LB
    APP --> LB
    
    LB --> API1
    LB --> API2
    LB --> API3
    
    API1 --> DIR_SVC
    API2 --> DIR_SVC
    API3 --> DIR_SVC
    
    DIR_SVC --> CRT_SVC
    DIR_SVC --> SYN_SVC
    DIR_SVC --> ANA_SVC
    DIR_SVC --> ARC_SVC
    DIR_SVC --> DSEC_SVC
    DIR_SVC --> DSRE_SVC
    
    ANA_SVC --> OPENAI
    ARC_SVC --> OPENAI
    DSEC_SVC --> OPENAI
    DSRE_SVC --> OPENAI
    
    API1 --> PG
    API2 --> PG
    API3 --> PG
    PG --> PG_REPLICA
    
    API1 --> REDIS
    API2 --> REDIS
    API3 --> REDIS
    
    API1 --> PROM
    API2 --> PROM
    API3 --> PROM
    PROM --> GRAF
    
    API1 --> ELK
    API2 --> ELK
    API3 --> ELK
    
    style DIR_SVC fill:#e1f5ff
    style CRT_SVC fill:#fff4e1
    style SYN_SVC fill:#e8f5e9
```

## Компоненты и их взаимодействие

### Ядро системы

1. **Director (Директор)**
   - Анализирует входящую задачу
   - Создает стратегию анализа
   - Координирует работу агентов
   - Управляет процессом

2. **Critic (Критик)**
   - Валидирует результаты агентов
   - Выявляет пропущенные проблемы
   - Проверяет согласованность
   - Оценивает критичность и качество

3. **Synthesizer (Синтезатор)**
   - Интегрирует результаты всех агентов
   - Приоритизирует проблемы
   - Генерирует финальный отчет
   - Экспортирует в различные форматы

### Агенты-специалисты

1. **Analyst Agent** - Системный аналитик
2. **Architect Agent** - Архитектор
3. **DevSecOps Agent** - Специалист по безопасности
4. **DevOps/SRE Agent** - Специалист по операциям

## Технологический стек

- **Backend**: Python 3.11+, FastAPI
- **Database**: PostgreSQL, Redis
- **AI/ML**: OpenAI API (GPT-4), DeepSeek API
- **Infrastructure**: Docker, Kubernetes
- **Monitoring**: Prometheus, Grafana, ELK Stack

## Принципы архитектуры

1. **Многоуровневая верификация** - Проверка с 4-х сторон + валидация
2. **Параллельная обработка** - Агенты работают одновременно
3. **API-First** - Все компоненты доступны через REST API
4. **Масштабируемость** - Горизонтальное масштабирование
5. **Надежность** - Обработка ошибок, retry механизмы

