import os
from typing import List
from pydantic import BaseModel, Field
from google import genai
from google.genai import types


# ==========================================
# 1. Pydantic Schemas for Structured Output
# ==========================================

class QuizQuestion(BaseModel):
    question: str = Field(description="The question text.")
    options: List[str] = Field(description="List of 4 multiple-choice options.")
    correct_option_index: int = Field(description="Zero-based index of the correct option (0-3).")
    explanation: str = Field(description="Brief explanation of why the correct answer is right.")


class Flashcard(BaseModel):
    front: str = Field(description="Concept or question on the front of the card.")
    back: str = Field(description="Clear, concise answer or definition on the back.")


class SprintPlan(BaseModel):
    day_1: str = Field(description="Day 1 action plan: core concepts & key terms review.")
    day_2: str = Field(description="Day 2 action plan: active recall & targeted practice.")
    day_3: str = Field(description="Day 3 action plan: final self-assessment & quick review.")


class StudyKitResponse(BaseModel):
    summary: str = Field(description="A comprehensive summary of the provided study notes.")
    keywords: List[str] = Field(description="5 to 10 key terms extracted from the notes.")
    sprint_plan: SprintPlan = Field(description="A structured 3-day sprint study plan.")
    quiz: List[QuizQuestion] = Field(description="3 to 5 active recall multiple-choice questions.")
    flashcards: List[Flashcard] = Field(description="3 to 5 flashcards for active revision.")


# ==========================================
# 2. Main Agent Execution Function
# ==========================================

def generate_study_kit(notes_text: str) -> dict:
    """
    Generates a complete study kit (summary, keywords, 3-day sprint plan, quiz, flashcards)
    from student study notes using Gemini 2.5 Flash.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set in the .env file.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an elite AI study tutor and learning strategist.
    Analyze the following student study notes and convert them into an actionable, high-yield Study Kit.

    Requirements:
    1. Provide a clear summary emphasizing core concepts.
    2. Extract 5 to 10 key terms/keywords.
    3. Create a structured 3-day study sprint plan (Day 1, Day 2, Day 3).
    4. Generate an active recall quiz (minimum 3-5 multiple-choice questions with 4 options each).
    5. Generate 3 to 5 flashcards for rapid revision.

    Student Notes:
    ----------------
    {notes_text}
    ----------------
    """

    # Try primary model first, with fallback to gemini-2.0-flash if needed
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=StudyKitResponse,
                temperature=0.2,
            ),
        )

        if not response.text:
            raise RuntimeError("Gemini model returned an empty response.")

        return StudyKitResponse.model_validate_json(response.text).model_dump()

    except Exception as e:
        # Fallback for accounts/regions using 2.0-flash
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=StudyKitResponse,
                    temperature=0.2,
                ),
            )
            return StudyKitResponse.model_validate_json(response.text).model_dump()
        except Exception as inner_e:
            raise RuntimeError(f"Failed to generate study kit with Gemini API: {str(inner_e)}")