import os
from google import genai

def generate_study_kit(notes: str):
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    prompt = f"""You are an expert AI study assistant. Based on the following notes, generate a comprehensive study kit including a summary, key terms, and practice quiz questions.

Notes:
{notes}
"""
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )
    return response.text
