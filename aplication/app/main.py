from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from dotenv import load_dotenv
load_dotenv()

from app.routes import patient

app = FastAPI()

# CORS (déjalo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 SERVIR EL HTML
@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")

# Rutas API
app.include_router(patient.router)