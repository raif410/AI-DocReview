# ✅ Правильный формат JSON для Swagger UI

## ❌ Что было не так в вашем JSON

У вас была **двойная вложенность** и лишние поля:

```json
{
  "document": {                    // ❌ НЕПРАВИЛЬНО: document должен быть строкой, а не объектом!
    "document": "...",
    "document_type": "markdown",
    "context": {}
  },
  "document_type": "markdown",     // ❌ Дублируется
  "context": {                     // ❌ Неправильный формат
    "additionalProp1": {}
  }
}
```

## ✅ Правильный формат

```json
{
  "document": "# Моя документация\n\n## Раздел 1\n\nТекст документации...",
  "document_type": "markdown",
  "context": {}
}
```

**Ключевые моменты:**
- `document` - это **строка** (текст в кавычках), НЕ объект
- `document_type` - это **строка** `"markdown"`
- `context` - это **объект** `{}` (может быть пустым)

---

## 📋 Правильная структура

```json
{
  "document": "ваш текст документации здесь",
  "document_type": "markdown",
  "context": {}
}
```

**Где:**
- `document` - просто текст в кавычках (не объект!)
- `document_type` - слово "markdown" в кавычках
- `context` - пустой объект `{}` или объект с данными

---

## 🎯 Как использовать в Swagger UI

1. Откройте http://localhost:8000/docs
2. Найдите `POST /api/v1/review/start`
3. Нажмите "Try it out"
4. В поле "Request body" выберите `application/json`
5. Заполните поля:
   - `document`: вставьте текст вашей документации
   - `document_type`: `"markdown"`
   - `context`: `{}`
6. Нажмите "Execute"

Swagger UI автоматически создаст правильный JSON!
