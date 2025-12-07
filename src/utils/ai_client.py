"""Клиент для работы с OpenAI API"""
import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from src.config import settings


class AIClient:
    """Клиент для взаимодействия с OpenAI API"""
    
    def __init__(self):
        api_key = settings.openai_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY не установлен")
        self.client = OpenAI(api_key=api_key)
        self.model = settings.openai_model
        self.temperature = settings.openai_temperature
        self.max_tokens = settings.openai_max_tokens
    
    async def analyze(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> str:
        """Выполнить анализ через LLM"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature or self.temperature,
            max_tokens=self.max_tokens
        )
        
        return response.choices[0].message.content
    
    async def analyze_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_format: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Выполнить структурированный анализ"""
        result = await self.analyze(prompt, system_prompt)
        # В реальной реализации здесь была бы парсинг JSON ответа
        # Для упрощения возвращаем текст
        return {"content": result, "raw": result}

