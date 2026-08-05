"""Local launcher for StudySprint AI.

Mounts the existing static `frontend/` directory onto the existing FastAPI
app (main.py) so the whole project runs on a single origin on localhost.
This file only adds a static mount; it does not modify any existing code.
"""
import os
from fastapi.staticfiles import StaticFiles
from main import app

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# Serve static frontend files (index.html, studio.html, etc.)
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
