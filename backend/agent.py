import os
import json
from google import genai
from google.genai import types

def generate_study_kit(notes: str) -> dict:
    client = genai.Client()
    
    prompt = f"""
    Analyze the following study notes and generate a comprehensive study kit.
    
    Notes:
    {notes}
    """
    
    system_instruction = """
    You are an expert tutor. Return a structured JSON object with the following fields:
    - summary: A clear, markdown-formatted summary of the notes.
    - flashcards: An array of objects, each containing 'term' and 'definition'.
    - quiz: An array of objects, each containing 'question' and 'answer'.
    - study_plan: An array of objects, each containing 'day' (e.g. Day 1) and 'focus'.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash",  # Active frontier model identifier
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
        ),
    )
    
    return json.loads(response.text)