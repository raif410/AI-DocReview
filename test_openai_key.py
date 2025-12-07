"""Тест API ключа OpenAI"""
import os
import sys
import io

# Настройка кодировки для Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from openai import OpenAI

# Проверяем наличие ключа
api_key = os.getenv("OPENAI_API_KEY") or None

if not api_key:
    # Пробуем загрузить из .env
    try:
        from src.config import settings
        api_key = settings.openai_api_key
    except:
        pass

if not api_key:
    print("❌ API ключ не найден!")
    print("\nПроверьте:")
    print("1. Файл .env существует и содержит OPENAI_API_KEY")
    print("2. Переменная окружения OPENAI_API_KEY установлена")
    sys.exit(1)

print(f"✅ API ключ найден (длина: {len(api_key)} символов)")
print(f"   Первые 10 символов: {api_key[:10]}...")

# Проверяем base_url для DeepSeek
base_url = os.getenv("OPENAI_BASE_URL") or None
try:
    from src.config import settings
    if settings.openai_base_url:
        base_url = settings.openai_base_url
except:
    pass

# Пробуем сделать тестовый запрос
try:
    if base_url and "deepseek" in base_url.lower():
        print(f"\n🧪 Тестирую подключение к DeepSeek API ({base_url})...")
        client = OpenAI(api_key=api_key, base_url=base_url)
        model = "deepseek-chat"
    else:
        print("\n🧪 Тестирую подключение к OpenAI API...")
        client = OpenAI(api_key=api_key)
        model = "gpt-3.5-turbo"
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": "Say 'Hello' if you can read this."}
        ],
        max_tokens=10
    )
    
    print("✅ API ключ работает!")
    print(f"   Ответ: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ Ошибка при тестировании API ключа:")
    print(f"   {type(e).__name__}: {e}")
    
    if "Invalid API key" in str(e) or "401" in str(e):
        print("\n⚠️  API ключ недействителен!")
        print("   Проверьте ключ на https://platform.openai.com/api-keys")
    elif "insufficient_quota" in str(e).lower():
        print("\n⚠️  Недостаточно средств на счету!")
        print("   Пополните баланс на https://platform.openai.com/account/billing")
    else:
        print("\n⚠️  Проверьте:")
        print("   1. Интернет соединение")
        print("   2. Правильность API ключа")
        print("   3. Баланс на счету OpenAI")
    
    sys.exit(1)

print("\n✅ Все проверки пройдены! API ключ работает корректно.")

