# Статус сервера DocReview AI

## ✅ Сервер успешно запущен!

### Доступные endpoints:

- **API Root**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **Swagger UI (Документация)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Исправленные проблемы:

1. ✅ Кодировка Unicode в Windows консоли
2. ✅ Ленивая инициализация компонентов
3. ✅ Правильная настройка uvicorn reload
4. ✅ Обработка отсутствия API ключа (с предупреждением)

### Запуск сервера:

```bash
python run.py
```

Или:

```bash
python -m src.main
```

### Тестирование:

```bash
# Health check
curl http://localhost:8000/health

# Или через PowerShell
Invoke-RestMethod -Uri http://localhost:8000/health
```

### Остановка сервера:

Нажмите `CTRL+C` в терминале, где запущен сервер.

