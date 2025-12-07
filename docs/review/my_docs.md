---

### **Документация (Версия 1.0 )**

```mermaid
erDiagram
    CLIENTS {
        INT client_id PK
        VARCHAR full_name
        DATE date_of_birth
        VARCHAR phone
        DECIMAL credit_score
        VARCHAR risk_category "NULL"
        VARCHAR manager_login FK
        VARCHAR last_scoring_date
        BOOL is_active
    }

    CLIENTS ||--o{ CREDIT_APPLICATIONS : "has"
    CLIENTS }o--|| EMPLOYEES : "assigned_to"

    CREDIT_APPLICATIONS {
        INT application_id PK
        INT client_id FK
        DECIMAL amount
        VARCHAR status
    }

    EMPLOYEES {
        VARCHAR login PK "format: 'login_domain'"
        VARCHAR fio
    }
```

**Описание изменений:**
1.  **Цель:** Добавить возможность хранения данных скоринга и внутренней аналитики.
2.  **Новые поля в таблице `CLIENTS`:**
    *   `credit_score` (DECIMAL) — рейтинг клиента, рассчитанный моделью.
    *   `risk_category` (VARCHAR) — категория риска ("низкий", "средний", "высокий"). **Может быть NULL.**
    *   `last_scoring_date` (VARCHAR) — дата последнего расчета скоринга.
    *   `manager_login` (VARCHAR) — логин ответственного менеджера. Ссылается на `EMPLOYEES.login`.
    *   `is_active` (BOOL) — флаг активности клиента для кредитования.
3.  **Бизнес-правила:**
    *   Скоринг обновляется еженедельно.
    *   Менеджер может быть не назначен (поле `manager_login` может быть `NULL`).
    *   Поле `risk_category` вычисляется на основе `credit_score`.

---