"""
CodeMentor AI Companion Service
Main FastAPI application entry point
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv

from .api.analysis import router as analysis_router
from .api.llm import router as llm_router

# Load environment variables
load_dotenv()

app = FastAPI(
    title="CodeMentor AI Companion",
    description="Desktop companion service for CodeMentor AI",
    version="0.0.1",
)

# Add CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(analysis_router, prefix="/api/analysis", tags=["analysis"])
app.include_router(llm_router, prefix="/api/llm", tags=["llm"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "CodeMentor AI Companion Service", "status": "running"}


@app.get("/health")
async def health_check():
    """Detailed health check"""
    from datetime import datetime
    return {
        "status": "healthy",
        "service": "codementor-companion",
        "version": "0.0.1",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication with IDE plugin"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Echo for now - implement actual message handling
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("WebSocket disconnected")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=port,
        reload=True,
        log_level="info"
    ) 