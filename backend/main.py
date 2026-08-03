import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from backend.agent import generate_study_kit

# Load environment variables from .env
load_dotenv()

app = FastAPI(
    title="StudySprint AI API",
    description="Backend service powering Gemini 2.5 Flash study kit generation.",
    version="1.0.0"
)

# Enable CORS for local development and web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request schemas
class NotesRequest(BaseModel):
    notes: str

class CheckoutRequest(BaseModel):
    plan_name: str
    price: str


# ==========================================
# API Endpoints
# ==========================================

@app.get("/")
async def root():
    """Redirect root access directly to the studio workspace."""
    return RedirectResponse(url="/app.html")


@app.post("/api/generate-kit")
async def handle_generate_study_kit(data: NotesRequest):
    """
    Accepts student notes and returns a structured AI study kit
    (summary, keywords, 3-day sprint plan, quiz, flashcards).
    """
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
    """
    Simulated checkout endpoint for plan upgrades.
    """
    return {
        "status": "success",
        "message": f"Successfully initiated checkout for {data.plan_name} plan ({data.price}).",
        "checkout_url": "#"
    }


# ==========================================
# Mount Frontend Static Files
# ==========================================

# Ensures all files in frontend/ (studio.html, app.html, styles.css, etc.) are served
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")