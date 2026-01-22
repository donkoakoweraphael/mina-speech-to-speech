from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import translation

app = FastAPI(title="Mina Speech-to-Speech API", version="0.1.0")

# CORS Configuration
origins = [
    "http://localhost:5173", # Vite default port
    "http://localhost:3000",
    "*" # For development simplicity
]

from fastapi.staticfiles import StaticFiles
import os

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create static dir if not exists
os.makedirs("static/audio", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(translation.router)

@app.get("/")
async def root():
    return {"message": "Mina Speech-to-Speech API is running"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
