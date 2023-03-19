import httpx
import openai
from app.core.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def chat_completion(prompt: str) -> str:
    """
    A function that sends a prompt to OpenAI's GPT-3.5-turbo model and returns the generated text.

    Args:
    prompt (str): The prompt to send to the GPT-3.5-turbo model

    Returns:
    str: The generated text from the GPT-3.5-turbo model

    Example:
    >>> import asyncio
    >>> from app.services.openai import chat_completion
    >>> asyncio.run(chat_completion("Hello, how are you?"))
    'I am doing well, thank you for asking. How about you?'
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}]
            },
            headers={"Authorization": f"Bearer {openai.api_key}"}
        )
    completion = response.json()
    return completion["choices"][0]["message"]["content"]
