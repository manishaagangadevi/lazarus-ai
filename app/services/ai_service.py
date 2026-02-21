import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)


def analyze_function_with_ai(function_source: str) -> str:
    prompt = f"""
You are a senior Python software engineer.

Analyze this function and answer clearly:

1. Is it safe to remove?
2. What risks could exist?
3. Short explanation.

Function:
{function_source}
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt,
    )

    return response.text