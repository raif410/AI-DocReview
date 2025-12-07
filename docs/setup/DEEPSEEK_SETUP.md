# 🔧 Настройка DeepSeek API

## ✅ API ключ настроен!

Ваш DeepSeek API ключ успешно сохранен в `.env` файле.

## 📋 Конфигурация

В файле `.env` установлено:
```
OPENAI_API_KEY=sk-e2d094cf041f4060b1caef7d1ca92f56
OPENAI_BASE_URL=https://api.deepseek.com
```

## 🧪 Проверка работы

Запустите тест:
```bash
python scripts/tools/test_openai_key.py
```

Должен вернуться: `✅ API ключ работает!`

## 🚀 Использование

Система автоматически использует DeepSeek API вместо OpenAI:
- Модель: `deepseek-chat`
- Base URL: `https://api.deepseek.com`
- API ключ: ваш DeepSeek ключ

## 📝 Примечания

- DeepSeek API совместим с OpenAI API
- Система автоматически определяет использование DeepSeek по `OPENAI_BASE_URL`
- Все функции работают так же, как с OpenAI

## 🔄 Перезапуск сервера

После настройки перезапустите сервер:
```bash
# Остановите текущий сервер (Ctrl+C)
# Запустите снова
python run.py
```

Готово! 🎉

