# CM-T2.3: Receive & Log Code from Plugin

## Summary
Implement code receiving and logging functionality to capture code snippets from the VS Code extension with structured logging and validation.

## Acceptance Criteria
- [ ] Analysis request handler registered with WebSocket manager
- [ ] Request validation and error handling implemented
- [ ] Code snippet processing pipeline established
- [ ] Response formatting and transmission back to client
- [ ] Request queuing and priority handling
- [ ] Performance metrics and logging

## Implementation Details

### Analysis Service (app/services/analysis_service.py)
```python
"""
Core analysis service for processing code snippets from VS Code extension.
Coordinates between different analysis engines and formats responses.
"""
import asyncio
import logging
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from pydantic import BaseModel, ValidationError

from app.services.websocket_manager import websocket_manager, AnalysisRequest, AnalysisResponse
from app.models.analysis import CodeSnippet, Violation, Suggestion, AnalysisResult

logger = logging.getLogger(__name__)

class AnalysisStats(BaseModel):
    """Statistics for analysis operations"""
    total_requests: int = 0
    successful_analyses: int = 0
    failed_analyses: int = 0
    average_processing_time: float = 0.0
    
class AnalysisService:
    """Core service for handling code analysis requests"""
    
    def __init__(self):
        # Analysis engines (will be implemented in Epic 3)
        self.rule_engine = None  # Will be injected from Epic 3
        self.ai_engine = None    # Will be injected from Epic 5
        
        # Request queue and processing
        self.request_queue: asyncio.Queue = asyncio.Queue()
        self.processing_requests: Dict[str, AnalysisRequest] = {}
        self.request_stats = AnalysisStats()
        
        # Configuration
        self.max_concurrent_analyses = 5
        self.request_timeout = 30  # seconds
        
        # Start background processing
        self._start_processors()
        
        # Register with WebSocket manager
        self._register_handlers()

    def _register_handlers(self):
        """Register analysis handlers with WebSocket manager"""
        websocket_manager.register_handler("analysis_request", self._handle_analysis_request)

    def _start_processors(self):
        """Start background request processors"""
        for i in range(self.max_concurrent_analyses):
            asyncio.create_task(self._process_requests())

    async def _handle_analysis_request(self, client_id: str, message):
        """Handle incoming analysis request from WebSocket"""
        try:
            # Parse the analysis request
            request_data = message.payload
            analysis_request = AnalysisRequest(**request_data)
            
            logger.info(f"Received analysis request {analysis_request.id} from {client_id}")
            
            # Add client info to request
            analysis_request.client_id = client_id
            analysis_request.received_at = datetime.now()
            
            # Queue for processing
            await self.request_queue.put(analysis_request)
            
            # Track the request
            self.processing_requests[analysis_request.id] = analysis_request
            self.request_stats.total_requests += 1
            
        except ValidationError as e:
            logger.error(f"Invalid analysis request from {client_id}: {e}")
            await self._send_error(client_id, "Invalid request format", str(e))
            
        except Exception as e:
            logger.error(f"Error handling analysis request from {client_id}: {e}")
            await self._send_error(client_id, "Internal error", str(e))

    async def _process_requests(self):
        """Background processor for analysis requests"""
        while True:
            try:
                # Get next request from queue
                request = await self.request_queue.get()
                
                logger.info(f"Processing analysis request {request.id}")
                start_time = time.time()
                
                # Process the request
                result = await self._analyze_code(request)
                
                # Calculate processing time
                processing_time = time.time() - start_time
                
                # Create response
                response = AnalysisResponse(
                    id=request.id,
                    violations=result.violations,
                    suggestions=result.suggestions,
                    processing_time=processing_time,
                    timestamp=int(datetime.now().timestamp() * 1000)
                )
                
                # Send response back to client
                await self._send_response(request.client_id, response)
                
                # Update statistics
                self.request_stats.successful_analyses += 1
                self._update_avg_processing_time(processing_time)
                
                # Clean up
                if request.id in self.processing_requests:
                    del self.processing_requests[request.id]
                
                logger.info(f"Completed analysis request {request.id} in {processing_time:.2f}s")
                
            except Exception as e:
                logger.error(f"Error processing analysis request: {e}")
                
                # Update error stats
                self.request_stats.failed_analyses += 1
                
                # Try to send error response if we have client info
                if hasattr(request, 'client_id'):
                    await self._send_error(request.client_id, "Analysis failed", str(e))

    async def _analyze_code(self, request: AnalysisRequest) -> AnalysisResult:
        """
        Analyze code snippets and return violations and suggestions.
        This is a placeholder that will integrate with Epic 3 (Rule Engine) 
        and Epic 5 (AI Integration).
        """
        violations = []
        suggestions = []
        
        # For now, return a placeholder response
        # This will be replaced with actual analysis engines in Epic 3 & 5
        
        for snippet in request.snippets:
            # Placeholder analysis - will be replaced with real engines
            if len(snippet.get('content', '')) > 100:
                violations.append({
                    'type': 'length',
                    'severity': 'warning',
                    'message': 'Consider breaking this into smaller functions',
                    'range': {
                        'start': {'line': 0, 'character': 0},
                        'end': {'line': 0, 'character': 50}
                    },
                    'rule': 'function-length',
                    'fixable': False
                })
            
            if 'TODO' in snippet.get('content', ''):
                suggestions.append({
                    'type': 'todo',
                    'message': 'Consider creating a GitHub issue for this TODO',
                    'range': {
                        'start': {'line': 0, 'character': 0},
                        'end': {'line': 0, 'character': 10}
                    },
                    'improvement': 'Replace TODO with proper issue tracking',
                    'confidence': 0.8
                })
        
        return AnalysisResult(
            violations=violations,
            suggestions=suggestions,
            metadata={
                'engine': 'placeholder',
                'version': '0.1.0',
                'processing_time': time.time()
            }
        )

    async def _send_response(self, client_id: str, response: AnalysisResponse):
        """Send analysis response back to client"""
        from app.services.websocket_manager import IPCMessage
        
        message = IPCMessage(
            type="analysis_response",
            payload=response.dict(),
            timestamp=int(datetime.now().timestamp() * 1000),
            id=f"response_{response.id}"
        )
        
        await websocket_manager.send_message(client_id, message)

    async def _send_error(self, client_id: str, error_type: str, error_message: str):
        """Send error response to client"""
        from app.services.websocket_manager import IPCMessage
        
        message = IPCMessage(
            type="analysis_error",
            payload={
                "error_type": error_type,
                "message": error_message,
                "timestamp": int(datetime.now().timestamp() * 1000)
            },
            timestamp=int(datetime.now().timestamp() * 1000),
            id=f"error_{int(datetime.now().timestamp() * 1000)}"
        )
        
        await websocket_manager.send_message(client_id, message)

    def _update_avg_processing_time(self, processing_time: float):
        """Update average processing time statistics"""
        total_successful = self.request_stats.successful_analyses
        current_avg = self.request_stats.average_processing_time
        
        # Calculate new average
        new_avg = ((current_avg * (total_successful - 1)) + processing_time) / total_successful
        self.request_stats.average_processing_time = new_avg

    def get_stats(self) -> Dict[str, Any]:
        """Get analysis service statistics"""
        return {
            "request_stats": self.request_stats.dict(),
            "queue_size": self.request_queue.qsize(),
            "active_requests": len(self.processing_requests),
            "max_concurrent": self.max_concurrent_analyses
        }

    def get_active_requests(self) -> List[str]:
        """Get list of currently processing request IDs"""
        return list(self.processing_requests.keys())

    async def cancel_request(self, request_id: str) -> bool:
        """Cancel a specific analysis request"""
        if request_id in self.processing_requests:
            del self.processing_requests[request_id]
            logger.info(f"Cancelled analysis request {request_id}")
            return True
        return False

# Global instance
analysis_service = AnalysisService()
```

### Analysis Models (app/models/analysis.py)
```python
"""
Data models for code analysis requests and responses.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class CodeSnippet(BaseModel):
    """Represents a code snippet for analysis"""
    content: str
    language: str
    uri: str
    range: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None

class Violation(BaseModel):
    """Represents a coding convention violation"""
    type: str
    severity: str  # 'error', 'warning', 'info'
    message: str
    range: Dict[str, Any]
    rule: str
    fixable: bool
    suggested_fix: Optional[str] = None

class Suggestion(BaseModel):
    """Represents an improvement suggestion"""
    type: str
    message: str
    range: Dict[str, Any]
    improvement: str
    confidence: float

class AnalysisResult(BaseModel):
    """Result of code analysis"""
    violations: List[Dict[str, Any]]
    suggestions: List[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]] = None
```

### FastAPI Router Integration (app/routers/analysis.py)
```python
"""
REST API endpoints for analysis service monitoring and control.
"""
from fastapi import APIRouter, HTTPException
from app.services.analysis_service import analysis_service

router = APIRouter()

@router.get("/analysis/stats")
async def get_analysis_stats():
    """Get analysis service statistics"""
    return analysis_service.get_stats()

@router.get("/analysis/active")
async def get_active_requests():
    """Get currently processing requests"""
    return {
        "active_requests": analysis_service.get_active_requests(),
        "count": len(analysis_service.get_active_requests())
    }

@router.post("/analysis/cancel/{request_id}")
async def cancel_analysis_request(request_id: str):
    """Cancel a specific analysis request"""
    success = await analysis_service.cancel_request(request_id)
    if not success:
        raise HTTPException(status_code=404, detail="Request not found")
    return {"message": f"Request {request_id} cancelled"}

@router.get("/analysis/health")
async def analysis_health_check():
    """Health check for analysis service"""
    stats = analysis_service.get_stats()
    return {
        "status": "healthy",
        "uptime": "calculated_uptime",  # Implement uptime tracking
        "queue_size": stats["queue_size"],
        "active_requests": stats["active_requests"]
    }
```

### Main App Integration (app/main.py updates)
```python
from app.routers import analysis
from app.services.analysis_service import analysis_service

# Include analysis router
app.include_router(analysis.router, prefix="/api/v1", tags=["analysis"])

@app.on_event("startup")
async def startup_event():
    """Application startup"""
    logger.info("CodeMentor Companion App starting up...")
    logger.info("Analysis service initialized")
```

## Technical Notes
- Implements async processing with configurable concurrency
- Provides comprehensive error handling and logging
- Includes performance monitoring and statistics
- Designed for integration with Epic 3 (Rule Engine) and Epic 5 (AI)
- Uses Pydantic models for data validation

## Dependencies
- FastAPI project setup from CM-T2.1
- WebSocket manager from CM-T2.2
- Will integrate with Epic 3 for rule-based analysis
- Will integrate with Epic 5 for AI-powered analysis

## Testing
- Request processing pipeline works correctly
- Error handling for invalid requests
- Performance under concurrent load
- WebSocket message routing
- Statistics tracking accuracy

## Estimated Hours
8-10 hours 