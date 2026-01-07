import os
from openai import OpenAI

def ask_gpt(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return "Chatbot service is not configured."

    try:
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an agriculture expert helping Indian farmers with crops, soil, fertilizers, and weather."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=150,
            temperature=0.4
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Chatbot error: {str(e)}"
