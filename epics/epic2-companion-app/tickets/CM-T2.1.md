# CM-T2.1: FastAPI Project Setup (Python)

## Summary
Initialize a modern Python project with FastAPI, proper dependency management, and development tooling.

## Acceptance Criteria
- [ ] Python project structure with virtual environment
- [ ] FastAPI application with basic endpoints
- [ ] Dependencies managed with requirements.txt or pyproject.toml
- [ ] Development tools configured (black, isort, flake8, mypy)
- [ ] Basic logging and configuration setup
- [ ] Docker support for containerization
- [ ] Project runs locally with uvicorn

## Implementation Details

### Project Structure
```
companion-app/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── messages.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── websocket_manager.py
│   └── utils/
│       ├── __init__.py
│       └── logger.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── requirements.txt
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### Main Application (app/main.py)
```python
"""
CodeMentor AI Companion App
FastAPI-based service for code analysis and convention checking
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.services.websocket_manager import WebSocketManager
from app.utils.logger import setup_logging

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize WebSocket manager
websocket_manager = WebSocketManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("CodeMentor AI Companion App starting...")
    yield
    logger.info("CodeMentor AI Companion App shutting down...")

# Create FastAPI application
app = FastAPI(
    title="CodeMentor AI Companion",
    description="Intelligent coding convention teacher backend service",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "CodeMentor AI Companion App", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "active_connections": websocket_manager.get_connection_count()
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for VS Code extension communication"""
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket_manager.handle_message(websocket, data)
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
        logger.info("Client disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
```

### Configuration (app/config.py)
```python
"""Application configuration using Pydantic settings"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    app_name: str = "CodeMentor AI Companion"
    host: str = "localhost"
    port: int = 8765
    debug: bool = True
    log_level: str = "INFO"
    
    # Future: OpenAI API configuration
    openai_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

### Message Models (app/models/messages.py)
```python
"""Pydantic models for WebSocket messages"""
from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime

class BaseMessage(BaseModel):
    """Base message structure"""
    type: str
    timestamp: datetime
    id: str

class DocumentChangeMessage(BaseMessage):
    """Message for document change events"""
    type: str = "document_changed"
    uri: str
    language: str
    change_count: int

class AnalysisRequestMessage(BaseMessage):
    """Message requesting code analysis"""
    type: str = "analysis_request"
    code: str
    language: str
    file_path: str

class AnalysisResultMessage(BaseMessage):
    """Message containing analysis results"""
    type: str = "analysis_result"
    violations: list[dict]
    suggestions: list[str]
    file_path: str

class PingMessage(BaseMessage):
    """Heartbeat ping message"""
    type: str = "ping"

class PongMessage(BaseMessage):
    """Heartbeat pong response"""
    type: str = "pong"
```

### Logger Setup (app/utils/logger.py)
```python
"""Logging configuration"""
import logging
import sys
from app.config import settings

def setup_logging():
    """Configure application logging"""
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('companion-app.log')
        ]
    )
```

### Dependencies (requirements.txt)
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
websockets==12.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.6
python-dotenv==1.0.0

# Development dependencies
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
black==23.11.0
isort==5.12.0
flake8==6.1.0
mypy==1.7.1
```

### Docker Configuration (Dockerfile)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Expose port
EXPOSE 8765

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8765"]
```

### Development Commands
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8765

# Run with Docker
docker build -t codementor-companion .
docker run -p 8765:8765 codementor-companion

# Development tools
black app/ tests/
isort app/ tests/
flake8 app/ tests/
mypy app/
pytest
```

## Technical Notes
- Use FastAPI's native async support for WebSocket handling
- Pydantic models ensure type safety for message passing
- Structured logging for debugging and monitoring
- Environment-based configuration for different deployments
- Docker support for consistent deployment

## Dependencies
- Python 3.9+
- FastAPI and related packages
- WebSocket support libraries

## Testing
- FastAPI application starts without errors
- Health endpoints return correct responses
- WebSocket connection can be established
- Basic message handling works
- Docker container builds and runs successfully

## Estimated Hours
6-8 hours 