import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from backend.agent import generate_study_kit

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

# Bulletproof path resolution for Vercel serverless environment
if os.path.exists("/var/task/frontend"):
    frontend_dir = "/var/task/frontend"
else:
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
# ==========================================
# 1. API Endpoints
# ==========================================

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

# ==========================================
# 2. Page Delivery Routes (Explicit File Serving)
# ==========================================

@app.get("/")
async def root():
    return FileResponse(os.path.join(frontend_dir, "app.html"))

@app.get("/app.html")
async def serve_app():
    return FileResponse(os.path.join(frontend_dir, "app.html"))

@app.get("/studio.html")
async def serve_studio():
    return FileResponse(os.path.join(frontend_dir, "studio.html"))

@app.get("/login.html")
async def serve_login():
    return FileResponse(os.path.join(frontend_dir, "login.html"))

@app.get("/signup.html")
async def serve_signup():
    return FileResponse(os.path.join(frontend_dir, "signup.html"))

@app.get("/404.html")
async def serve_404():
    return FileResponse(os.path.join(frontend_dir, "404.html"))

# ==========================================
# 3. Static Files Directory Mount
# Serves JS, CSS, and other static assets (e.g., firebase-config.js)
# ==========================================

app.mount("/", StaticFiles(directory=frontend_dir), name="static")