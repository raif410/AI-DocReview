# Настройка OpenAI API ключа

## Вариант 1: Создание .env файла (Рекомендуется)

Создайте файл `.env` в корне проекта со следующим содержимым:

```env
OPENAI_API_KEY=your-api-key-here
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
```

## Вариант 2: PowerShell (для текущей сессии)

```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

## Вариант 3: Windows CMD

```cmd
set OPENAI_API_KEY=your-api-key-here
```

## Проверка

После настройки проверьте:

```bash
python -c "from src.config import settings; print('API Key:', 'OK' if settings.openai_api_key else 'NOT SET')"
```

## Важно!

⚠️ **НЕ КОММИТЬТЕ .env файл в git!** Он уже добавлен в `.gitignore`.

## Получение API ключа

1. Перейдите на https://platform.openai.com/api-keys
2. Войдите в свой аккаунт
3. Нажмите "Create new secret key"
4. Скопируйте ключ и сохраните его в `.env` файле

