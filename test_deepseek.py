"""Простой тест DeepSeek API"""
import sys
import io

# Настройка кодировки
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from openai import OpenAI

# Читаем ключ напрямую из .env
api_key = "sk-e2d094cf041f4060b1caef7d1ca92f56"
base_url = "https://api.deepseek.com"

print("=" * 60)
print("Тест DeepSeek API")
print("=" * 60)
print(f"\nAPI Key: {api_key[:20]}...")
print(f"Base URL: {base_url}")

try:
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    print("\n🧪 Тестирую подключение...")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": "Say 'Hello' if you can read this."}
        ],
        max_tokens=10
    )
    
    print("✅ API ключ работает!")
    print(f"   Ответ: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ Ошибка: {type(e).__name__}: {e}")
    
    if "401" in str(e) or "Authentication" in str(e):
        print("\n⚠️  Проблема с аутентификацией")
        print("   Проверьте правильность API ключа")
    elif "403" in str(e):
        print("\n⚠️  Доступ запрещен")
        print("   Проверьте баланс или права доступа")
    else:
        print("\n⚠️  Проверьте:")
        print("   1. Интернет соединение")
        print("   2. Правильность API ключа")
        print("   3. Баланс на счету DeepSeek")

