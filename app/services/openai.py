import openai

openai.api_key = "your_openai_api_key"

def chat_completion(prompt: str):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message['content']
