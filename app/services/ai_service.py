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

Analyze this function and return your answer STRICTLY in this format:

SAFE_TO_REMOVE: (Yes / No / Conditional)
RISK_LEVEL: (Low / Medium / High)
CONFIDENCE_SCORE: (0-100)
EXPLANATION: (short explanation)

Function:
{function_source}
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt,
    )

    return response.text