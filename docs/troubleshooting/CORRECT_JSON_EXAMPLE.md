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
  "document": "# my_docs.md\n\n---\n\n### **Документация (Версия 1.0 )**\n\n...",
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

## 🎯 Используйте скрипт - он выведет правильный формат!

```bash
python scripts/cli/show_file_content_json.py
```

Скрипт автоматически создаст правильный JSON!

