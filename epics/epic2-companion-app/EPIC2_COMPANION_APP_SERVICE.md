# Epic 2: Desktop Companion App - Core Service & IPC Server

Backend FastAPI service that receives code from the plugin, performs analysis, and provides the foundation for AI-powered convention teaching.

## Completed Tasks

- [ ] None yet - starting fresh implementation

## In Progress Tasks

- [ ] CM-T2.1: FastAPI Project Setup (Python)
- [ ] CM-T2.2: Establish IPC Server in FastAPI
- [ ] CM-T2.3: Receive & Log Code from Plugin
- [ ] CM-T2.4: Basic Service Health Check
- [ ] CM-T2.5: Companion App Packaging (Basic)

## Future Tasks

- [ ] Advanced logging and monitoring
- [ ] Configuration management system
- [ ] Database integration for caching
- [ ] Multi-client support

## Implementation Plan

### Architecture Overview
The desktop companion app will be built using [FastAPI](https://fastapi.tiangolo.com/), a modern Python web framework that provides automatic API documentation, type validation, and high performance. The service will run locally and communicate with the Cursor plugin via WebSocket or HTTP endpoints.

### Technical Stack
- **Language**: Python 3.11+
- **Framework**: FastAPI with Uvicorn ASGI server
- **Communication**: WebSocket (websockets library) + HTTP REST API
- **Validation**: Pydantic models for request/response validation
- **Logging**: Python logging with structured output
- **Packaging**: PyInstaller for standalone executable
- **Testing**: pytest with FastAPI TestClient

## Detailed Ticket Implementation

### CM-T2.1: FastAPI Project Setup (Python)

**Technical Requirements:**
- Python 3.11+ with virtual environment
- FastAPI framework with automatic OpenAPI documentation
- Uvicorn ASGI server for production-ready serving
- Pydantic for data validation and serialization
- Structured project layout following FastAPI best practices

**Implementation Steps:**
1. Create Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install core dependencies:
   ```bash
   pip install fastapi[all] uvicorn[standard] pydantic websockets python-multipart
   ```

3. Create project structure:
   ```
   codementor-companion/
   ├── app/
   │   ├── __init__.py
   │   ├── main.py              # FastAPI app entry point
   │   ├── api/                 # API route modules
   │   │   ├── __init__.py
   │   │   └── v1/
   │   ├── core/                # Core business logic
   │   │   ├── __init__.py
   │   │   └── config.py        # Application configuration
   │   ├── models/              # Pydantic models
   │   │   ├── __init__.py
   │   │   └── requests.py      # Request/response models
   │   └── services/            # Business logic services
   │       └── __init__.py
   ├── requirements.txt         # Python dependencies
   ├── pyproject.toml          # Project configuration
   └── README.md
   ```

4. Create basic FastAPI application:
   ```python
   # app/main.py
   from fastapi import FastAPI
   from fastapi.middleware.cors import CORSMiddleware
   
   app = FastAPI(
       title="CodeMentor AI Companion",
       description="Backend service for CodeMentor AI convention analysis",
       version="0.1.0"
   )
   
   # Configure CORS for local development
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # Configure appropriately for production
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   
   @app.get("/")
   async def root():
       return {"message": "CodeMentor AI Companion Service", "status": "running"}
   ```

**Files to Create:**
- `app/main.py` - FastAPI application entry point
- `requirements.txt` - Python dependencies
- `pyproject.toml` - Project metadata and build configuration
- `app/core/config.py` - Application configuration settings

### CM-T2.2: Establish IPC Server in FastAPI

**Technical Requirements:**
- WebSocket server endpoint for real-time communication
- HTTP REST endpoints for request/response patterns
- Connection management and client tracking
- Message routing and protocol handling
- Error handling and connection recovery

**Implementation Steps:**
1. Install WebSocket dependencies and create connection manager
2. Create WebSocket endpoint for real-time communication
3. Create HTTP IPC endpoints for request/response patterns
4. Configure server binding and connection management
5. Implement message routing and protocol handling

**Files to Create:**
- `app/services/websocket_manager.py` - WebSocket connection management
- `app/api/v1/websocket.py` - WebSocket endpoints
- `app/api/v1/ipc.py` - HTTP IPC endpoints
- `app/core/config.py` - Server configuration

### CM-T2.3: Receive & Log Code from Plugin

**Technical Requirements:**
- Pydantic models for code analysis requests
- Structured logging with correlation IDs
- Request validation and sanitization
- File-based logging with rotation
- Performance monitoring and metrics

**Implementation Steps:**
1. Create comprehensive Pydantic models for all request types
2. Configure structured logging with JSON format and rotation
3. Implement code receiving endpoint with validation
4. Add performance monitoring and correlation tracking
5. Create error handling and response formatting

**Files to Create:**
- `app/models/requests.py` - Pydantic request/response models
- `app/core/logging.py` - Structured logging configuration
- `app/services/code_processor.py` - Code analysis processing service
- `logs/` - Directory for log files

### CM-T2.4: Basic Service Health Check

**Technical Requirements:**
- Health check endpoints for service monitoring
- System resource monitoring (CPU, memory)
- Connection status reporting
- Service dependency checks
- Prometheus-compatible metrics (future)

**Implementation Steps:**
1. Create health check models and status enums
2. Implement health check service with system monitoring
3. Create comprehensive health check endpoints
4. Add readiness and liveness probes
5. Implement service dependency monitoring

**Files to Create:**
- `app/models/health.py` - Health check data models
- `app/services/health_service.py` - Health monitoring service
- `app/api/v1/health.py` - Health check endpoints

### CM-T2.5: Companion App Packaging (Basic)

**Technical Requirements:**
- PyInstaller for creating standalone executables
- Cross-platform support (Windows, macOS, Linux)
- Dependency bundling and optimization
- Basic installer scripts
- Configuration file handling

**Implementation Steps:**
1. Install PyInstaller and create build specification
2. Create cross-platform build scripts
3. Implement configuration management system
4. Create startup scripts and service management
5. Add basic installation and setup instructions

**Files to Create:**
- `codementor-companion.spec` - PyInstaller build specification
- `scripts/build.sh` - Linux/macOS build script
- `scripts/build.bat` - Windows build script
- `scripts/start_companion.py` - Service startup script
- `app/config_template.py` - Configuration management

## Relevant Files

- `app/main.py` - FastAPI application entry point ✅
- `app/services/websocket_manager.py` - WebSocket connection management ✅
- `app/api/v1/ipc.py` - IPC communication endpoints ✅
- `app/services/code_processor.py` - Code analysis processing ✅
- `app/services/health_service.py` - Health monitoring service ✅
- `app/models/requests.py` - Pydantic data models ✅
- `app/core/config.py` - Application configuration ✅
- `app/core/logging.py` - Structured logging setup ✅
- `requirements.txt` - Python dependencies ✅
- `codementor-companion.spec` - PyInstaller build specification ✅

## Technical Considerations

### Performance Optimization
- Use Uvicorn with multiple workers for production
- Implement connection pooling for database operations
- Add request/response compression
- Implement caching for frequently accessed data

### Security
- Input validation with Pydantic models
- Rate limiting for API endpoints
- Secure WebSocket connections
- Local-only binding (127.0.0.1)
- Request size limits to prevent DoS

### Monitoring & Observability
- Structured logging with correlation IDs
- Health check endpoints for monitoring
- Performance metrics collection
- Error tracking and alerting

### Error Handling
- Graceful degradation for service failures
- Proper HTTP status codes
- Detailed error messages for debugging
- Circuit breaker pattern for external dependencies

### Scalability Considerations
- Stateless service design
- Horizontal scaling capability
- Database connection pooling
- Async/await for I/O operations 