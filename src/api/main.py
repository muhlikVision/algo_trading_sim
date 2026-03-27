from fastapi import FastAPI
from src.api.routes import router

# Initialize the FastAPI app (This is the 'app' Uvicorn is looking for!)
app = FastAPI(
    title="Algorithmic Trading & Sentiment API",
    description="A RAG-powered backtesting engine using NVIDIA Nemotron.",
    version="1.0.0"
)

# Include our simulation routes
app.include_router(router)

# A simple health-check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "nvidia/nemotron-4-340b-instruct"}