import openai
from app.core.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def chat_completion(prompt: str):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message['content']
