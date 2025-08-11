import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def generate_tsd_document(messages):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file or environment")

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f" OpenAI API error: {e}")
        return ""
