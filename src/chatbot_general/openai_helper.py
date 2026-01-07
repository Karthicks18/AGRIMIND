import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_gpt35(prompt: str):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an agriculture expert for Indian farmers."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.4
        )
        return response.choices[0].message.content
    except Exception as e:
        return None
