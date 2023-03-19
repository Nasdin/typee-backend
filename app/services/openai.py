import httpx
import openai

from app.core.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


async def chat_completion(prompt: str):
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
