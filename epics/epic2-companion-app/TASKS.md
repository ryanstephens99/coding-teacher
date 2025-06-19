# Epic 2: Desktop Companion App Service Implementation

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
- [ ] Performance optimization
- [ ] Security hardening

## Implementation Plan

### Architecture Overview
The desktop companion app will be built using FastAPI, a modern Python web framework that provides automatic API documentation, type validation, and high performance. The service will run locally and communicate with the Cursor plugin via WebSocket or HTTP endpoints.

### Technical Stack
- **Language**: Python 3.11+
- **Framework**: FastAPI with Uvicorn ASGI server
- **Communication**: WebSocket (websockets library) + HTTP REST API
- **Validation**: Pydantic models for request/response validation
- **Logging**: Python logging with structured output
- **Packaging**: PyInstaller for standalone executable
- **Testing**: pytest with FastAPI TestClient

### Data Flow
1. VS Code extension sends code changes via WebSocket
2. FastAPI receives and validates request data
3. Code is logged and queued for analysis
4. Analysis results are formatted and sent back
5. Health checks monitor service status
6. Packaging creates distributable executable

### Performance Considerations
- Async/await for I/O operations
- Request validation with Pydantic
- Structured logging for debugging
- Connection pooling for scalability
- Memory-efficient processing

## Relevant Files

### Core Application Files
- `app/main.py` - FastAPI application entry point ✅
- `app/config.py` - Application configuration ✅
- `requirements.txt` - Python dependencies ✅
- `pyproject.toml` - Project metadata and build configuration ✅

### Service Layer
- `app/services/websocket_manager.py` - WebSocket connection management ✅
- `app/services/analysis_service.py` - Code analysis processing ✅
- `app/services/health_service.py` - Health monitoring service ✅

### API Layer
- `app/api/v1/websocket.py` - WebSocket endpoints ✅
- `app/api/v1/ipc.py` - HTTP IPC endpoints ✅
- `app/api/v1/health.py` - Health check endpoints ✅

### Data Models
- `app/models/requests.py` - Pydantic request/response models ✅
- `app/models/messages.py` - WebSocket message models ✅
- `app/models/analysis.py` - Analysis data structures ✅

### Utilities
- `app/utils/logger.py` - Logging configuration ✅
- `app/utils/validation.py` - Input validation utilities ✅

### Packaging
- `companion.spec` - PyInstaller build specification ✅
- `scripts/build.sh` - Linux/macOS build script ✅
- `scripts/build.bat` - Windows build script ✅
- `scripts/start_companion.py` - Service startup script ✅

### Testing
- `tests/test_main.py` - Main application tests ✅
- `tests/test_websocket.py` - WebSocket functionality tests ✅
- `tests/test_analysis.py` - Analysis service tests ✅

## Technical Implementation Details

### CM-T2.1: FastAPI Project Setup (Python)
- Initialize Python project with virtual environment
- Configure FastAPI with automatic OpenAPI documentation
- Set up Uvicorn ASGI server configuration
- Create project structure following best practices
- Configure development tools (black, isort, flake8, mypy)
- **Estimated Hours**: 6-8 hours

### CM-T2.2: Establish IPC Server in FastAPI
- Implement WebSocket server endpoint for real-time communication
- Create HTTP REST endpoints for request/response patterns
- Set up connection management and client tracking
- Implement message routing and protocol handling
- Add error handling and connection recovery
- **Estimated Hours**: 8-10 hours

### CM-T2.3: Receive & Log Code from Plugin
- Create Pydantic models for code analysis requests
- Configure structured logging with correlation IDs
- Implement code receiving endpoint with validation
- Add performance monitoring and correlation tracking
- Create error handling and response formatting
- **Estimated Hours**: 6-8 hours

### CM-T2.4: Basic Service Health Check
- Create health check endpoints for service monitoring
- Implement system resource monitoring (CPU, memory)
- Add connection status reporting
- Create service dependency checks
- Implement readiness and liveness probes
- **Estimated Hours**: 4-6 hours

### CM-T2.5: Companion App Packaging (Basic)
- Configure PyInstaller for standalone executables
- Create cross-platform build scripts
- Implement basic configuration management
- Create startup scripts and service management
- Add installation and setup instructions
- **Estimated Hours**: 6-8 hours

## Dependencies

### External Dependencies
- `fastapi[all]` - FastAPI framework with all optional dependencies
- `uvicorn[standard]` - ASGI server with standard extras
- `websockets` - WebSocket client and server library
- `pydantic` - Data validation and serialization
- `python-multipart` - Form data parsing
- `pytest` - Testing framework
- `pyinstaller` - Executable packaging

### Internal Dependencies
- Epic 1 VS Code extension for client communication
- WebSocket endpoint (localhost:8765)
- Proper network connectivity for local communication

## Testing Strategy

### Unit Tests
- FastAPI endpoint testing with TestClient
- WebSocket connection and message handling
- Pydantic model validation
- Service initialization and configuration

### Integration Tests
- End-to-end communication with VS Code extension
- WebSocket connection lifecycle testing
- Error scenarios and recovery testing
- Health check endpoint validation

### Performance Tests
- Concurrent connection handling
- Message throughput testing
- Memory usage monitoring
- Service startup and shutdown times

## Security Considerations

- Input validation with Pydantic models
- Localhost-only binding (127.0.0.1)
- Request size limits to prevent DoS
- Secure WebSocket connections
- No sensitive data logging
- Rate limiting for API endpoints

## Deployment

### Development
- Virtual environment setup
- Hot reload with uvicorn --reload
- Development configuration
- Local testing with VS Code extension

### Production
- Standalone executable with PyInstaller
- Service management scripts
- Production configuration
- System service integration

## Success Criteria

- [ ] FastAPI service starts without errors
- [ ] WebSocket connections work reliably
- [ ] Code receiving and logging functions correctly
- [ ] Health checks provide accurate status
- [ ] Executable packages successfully
- [ ] VS Code extension can connect and communicate
- [ ] Service handles errors gracefully
- [ ] Performance meets requirements for normal use 