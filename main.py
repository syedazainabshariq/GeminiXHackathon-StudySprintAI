import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from agent import generate_study_kit

load_dotenv()

app = FastAPI(
    title="StudySprint AI API",
    description="Backend service powering Gemini 2.5 Flash study kit generation.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NotesRequest(BaseModel):
    notes: str

class CheckoutRequest(BaseModel):
    plan_name: str
    price: str

@app.post("/api/generate-kit")
async def handle_generate_study_kit(data: NotesRequest):
    if not data.notes or len(data.notes.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Please provide study notes with at least 10 characters."
        )

    try:
        result = generate_study_kit(data.notes)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate study kit: {str(e)}"
        )

@app.post("/api/checkout")
async def handle_checkout(data: CheckoutRequest):
    return {
        "status": "success",
        "message": f"Successfully initiated checkout for {data.plan_name} plan ({data.price}).",
        "checkout_url": "#"
    }