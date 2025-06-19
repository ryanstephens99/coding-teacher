# CM-T2.2: WebSocket IPC Server Setup

## Summary
Implement WebSocket-based IPC server in FastAPI to communicate with the VS Code extension.

## Acceptance Criteria
- [ ] FastAPI WebSocket endpoint for real-time communication
- [ ] Connection management with automatic reconnection support
- [ ] Message routing and handling system
- [ ] Connection lifecycle management (connect/disconnect events)
- [ ] Error handling and graceful degradation
- [ ] Message queuing for disconnected clients

## Implementation Details

### WebSocket Manager (app/services/websocket_manager.py)
```python
"""
WebSocket connection manager for handling IPC with VS Code extension.
Based on modern FastAPI WebSocket patterns and best practices.
"""
import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)

class IPCMessage(BaseModel):
    """Standard IPC message format"""
    type: str
    payload: Any
    timestamp: int
    id: str

class AnalysisRequest(BaseModel):
    """Analysis request from VS Code extension"""
    id: str
    snippets: List[Dict[str, Any]]
    document: Dict[str, Any]
    priority: str = "normal"

class AnalysisResponse(BaseModel):
    """Analysis response to VS Code extension"""
    id: str
    violations: List[Dict[str, Any]]
    suggestions: List[Dict[str, Any]]
    processing_time: float
    timestamp: int

class ConnectionInfo(BaseModel):
    """Connection metadata"""
    websocket: WebSocket
    client_id: str
    connected_at: datetime
    last_ping: Optional[datetime] = None
    message_count: int = 0

class WebSocketManager:
    """Manages WebSocket connections and message routing"""
    
    def __init__(self):
        # Active connections
        self.connections: Dict[str, ConnectionInfo] = {}
        
        # Message handlers
        self.message_handlers: Dict[str, Callable] = {}
        
        # Message queue for disconnected clients
        self.message_queue: Dict[str, List[IPCMessage]] = {}
        
        # Configuration
        self.max_queue_size = 100
        self.ping_interval = 30  # seconds
        self.connection_timeout = 60  # seconds
        
        # Register default handlers
        self._register_default_handlers()
        
        # Start background tasks
        self._start_background_tasks()

    def _register_default_handlers(self):
        """Register default message handlers"""
        self.register_handler("ping", self._handle_ping)
        self.register_handler("analysis_request", self._handle_analysis_request)

    def _start_background_tasks(self):
        """Start background maintenance tasks"""
        asyncio.create_task(self._ping_clients())
        asyncio.create_task(self._cleanup_stale_connections())

    async def connect(self, websocket: WebSocket, client_id: str) -> bool:
        """Accept a new WebSocket connection"""
        try:
            await websocket.accept()
            
            connection_info = ConnectionInfo(
                websocket=websocket,
                client_id=client_id,
                connected_at=datetime.now()
            )
            
            self.connections[client_id] = connection_info
            
            logger.info(f"Client {client_id} connected. Total connections: {len(self.connections)}")
            
            # Send any queued messages
            await self._flush_message_queue(client_id)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to accept connection from {client_id}: {e}")
            return False

    async def disconnect(self, client_id: str):
        """Handle client disconnection"""
        if client_id in self.connections:
            connection_info = self.connections[client_id]
            
            try:
                await connection_info.websocket.close()
            except Exception as e:
                logger.warning(f"Error closing WebSocket for {client_id}: {e}")
            
            del self.connections[client_id]
            logger.info(f"Client {client_id} disconnected. Total connections: {len(self.connections)}")

    async def send_message(self, client_id: str, message: IPCMessage) -> bool:
        """Send message to specific client"""
        if client_id not in self.connections:
            # Queue message for when client reconnects
            await self._queue_message(client_id, message)
            return False

        connection_info = self.connections[client_id]
        
        try:
            message_json = message.json()
            await connection_info.websocket.send_text(message_json)
            
            connection_info.message_count += 1
            logger.debug(f"Sent message to {client_id}: {message.type}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send message to {client_id}: {e}")
            await self.disconnect(client_id)
            return False

    async def broadcast_message(self, message: IPCMessage, exclude_client: Optional[str] = None):
        """Broadcast message to all connected clients"""
        disconnected_clients = []
        
        for client_id, connection_info in self.connections.items():
            if exclude_client and client_id == exclude_client:
                continue
                
            success = await self.send_message(client_id, message)
            if not success:
                disconnected_clients.append(client_id)
        
        # Clean up disconnected clients
        for client_id in disconnected_clients:
            await self.disconnect(client_id)

    async def handle_message(self, client_id: str, message_data: str):
        """Handle incoming message from client"""
        try:
            # Parse message
            message_dict = json.loads(message_data)
            message = IPCMessage(**message_dict)
            
            # Update connection info
            if client_id in self.connections:
                self.connections[client_id].message_count += 1
            
            # Route to appropriate handler
            handler = self.message_handlers.get(message.type)
            if handler:
                await handler(client_id, message)
            else:
                logger.warning(f"No handler for message type: {message.type}")
                
        except ValidationError as e:
            logger.error(f"Invalid message format from {client_id}: {e}")
            await self._send_error(client_id, "Invalid message format", str(e))
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON from {client_id}: {e}")
            await self._send_error(client_id, "Invalid JSON", str(e))
            
        except Exception as e:
            logger.error(f"Error handling message from {client_id}: {e}")
            await self._send_error(client_id, "Internal error", str(e))

    def register_handler(self, message_type: str, handler: Callable):
        """Register a message handler"""
        self.message_handlers[message_type] = handler
        logger.debug(f"Registered handler for message type: {message_type}")

    async def _handle_ping(self, client_id: str, message: IPCMessage):
        """Handle ping message"""
        if client_id in self.connections:
            self.connections[client_id].last_ping = datetime.now()
        
        # Send pong response
        pong_message = IPCMessage(
            type="pong",
            payload={"timestamp": message.timestamp},
            timestamp=int(datetime.now().timestamp() * 1000),
            id=f"pong_{message.id}"
        )
        
        await self.send_message(client_id, pong_message)

    async def _handle_analysis_request(self, client_id: str, message: IPCMessage):
        """Handle analysis request - to be implemented by analysis service"""
        logger.info(f"Received analysis request from {client_id}: {message.id}")
        
        # This will be implemented in CM-T2.3 (Analysis Request Handler)
        # For now, just acknowledge receipt
        ack_message = IPCMessage(
            type="analysis_request_ack",
            payload={"request_id": message.payload.get("id", "unknown")},
            timestamp=int(datetime.now().timestamp() * 1000),
            id=f"ack_{message.id}"
        )
        
        await self.send_message(client_id, ack_message)

    async def _queue_message(self, client_id: str, message: IPCMessage):
        """Queue message for disconnected client"""
        if client_id not in self.message_queue:
            self.message_queue[client_id] = []
        
        queue = self.message_queue[client_id]
        
        # Remove oldest messages if queue is full
        if len(queue) >= self.max_queue_size:
            removed_messages = queue[:len(queue) - self.max_queue_size + 1]
            queue = queue[len(queue) - self.max_queue_size + 1:]
            self.message_queue[client_id] = queue
            
            logger.warning(f"Message queue full for {client_id}, removed {len(removed_messages)} messages")
        
        queue.append(message)
        logger.debug(f"Queued message for {client_id}: {message.type}")

    async def _flush_message_queue(self, client_id: str):
        """Send all queued messages to reconnected client"""
        if client_id not in self.message_queue:
            return
        
        queue = self.message_queue[client_id]
        if not queue:
            return
        
        logger.info(f"Flushing {len(queue)} queued messages for {client_id}")
        
        for message in queue:
            await self.send_message(client_id, message)
        
        # Clear queue
        del self.message_queue[client_id]

    async def _send_error(self, client_id: str, error_type: str, error_message: str):
        """Send error message to client"""
        error_msg = IPCMessage(
            type="error",
            payload={
                "error_type": error_type,
                "message": error_message
            },
            timestamp=int(datetime.now().timestamp() * 1000),
            id=f"error_{int(datetime.now().timestamp() * 1000)}"
        )
        
        await self.send_message(client_id, error_msg)

    async def _ping_clients(self):
        """Periodically ping all clients"""
        while True:
            try:
                await asyncio.sleep(self.ping_interval)
                
                ping_message = IPCMessage(
                    type="ping",
                    payload={"server_time": int(datetime.now().timestamp() * 1000)},
                    timestamp=int(datetime.now().timestamp() * 1000),
                    id=f"ping_{int(datetime.now().timestamp() * 1000)}"
                )
                
                await self.broadcast_message(ping_message)
                
            except Exception as e:
                logger.error(f"Error in ping task: {e}")

    async def _cleanup_stale_connections(self):
        """Clean up stale connections"""
        while True:
            try:
                await asyncio.sleep(60)  # Check every minute
                
                now = datetime.now()
                stale_clients = []
                
                for client_id, connection_info in self.connections.items():
                    # Check if connection is stale
                    if connection_info.last_ping:
                        time_since_ping = (now - connection_info.last_ping).total_seconds()
                        if time_since_ping > self.connection_timeout:
                            stale_clients.append(client_id)
                    else:
                        # No ping received yet, check connection age
                        connection_age = (now - connection_info.connected_at).total_seconds()
                        if connection_age > self.connection_timeout:
                            stale_clients.append(client_id)
                
                # Disconnect stale clients
                for client_id in stale_clients:
                    logger.warning(f"Disconnecting stale client: {client_id}")
                    await self.disconnect(client_id)
                    
            except Exception as e:
                logger.error(f"Error in cleanup task: {e}")

    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        return {
            "total_connections": len(self.connections),
            "clients": [
                {
                    "client_id": client_id,
                    "connected_at": info.connected_at.isoformat(),
                    "message_count": info.message_count,
                    "last_ping": info.last_ping.isoformat() if info.last_ping else None
                }
                for client_id, info in self.connections.items()
            ],
            "queued_messages": {
                client_id: len(queue)
                for client_id, queue in self.message_queue.items()
            }
        }

# Global instance
websocket_manager = WebSocketManager()
```

### FastAPI WebSocket Endpoint (app/routers/websocket.py)
```python
"""
WebSocket router for IPC communication
"""
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.services.websocket_manager import websocket_manager

logger = logging.getLogger(__name__)
router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, client_id: str = Query(...)):
    """Main WebSocket endpoint for IPC communication"""
    
    logger.info(f"WebSocket connection attempt from client: {client_id}")
    
    # Accept connection
    connection_success = await websocket_manager.connect(websocket, client_id)
    if not connection_success:
        logger.error(f"Failed to establish connection with {client_id}")
        return
    
    try:
        # Message handling loop
        while True:
            # Receive message from client
            message_data = await websocket.receive_text()
            
            # Handle the message
            await websocket_manager.handle_message(client_id, message_data)
            
    except WebSocketDisconnect:
        logger.info(f"Client {client_id} disconnected normally")
        
    except Exception as e:
        logger.error(f"Unexpected error with client {client_id}: {e}")
        
    finally:
        # Clean up connection
        await websocket_manager.disconnect(client_id)

@router.get("/ws/stats")
async def get_websocket_stats():
    """Get WebSocket connection statistics"""
    return websocket_manager.get_connection_stats()
```

### Integration with Main App (app/main.py updates)
```python
from fastapi import FastAPI
from app.routers import websocket
from app.services.websocket_manager import websocket_manager

app = FastAPI(title="CodeMentor Companion App")

# Include WebSocket router
app.include_router(websocket.router, prefix="/api/v1", tags=["websocket"])

@app.on_event("startup")
async def startup_event():
    """Application startup"""
    logger.info("CodeMentor Companion App starting up...")
    
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    logger.info("CodeMentor Companion App shutting down...")
    
    # Disconnect all WebSocket clients
    for client_id in list(websocket_manager.connections.keys()):
        await websocket_manager.disconnect(client_id)
```

## Technical Notes
- Implements robust connection management with automatic cleanup
- Supports message queuing for offline clients
- Provides comprehensive error handling and logging
- Uses Pydantic models for message validation
- Includes connection statistics and monitoring

## Dependencies
- FastAPI project setup from CM-T2.1
- WebSocket support in FastAPI
- Pydantic for data validation

## Testing
- WebSocket connections established successfully
- Message routing works correctly
- Connection lifecycle managed properly
- Error scenarios handled gracefully
- Message queuing functions as expected

## Estimated Hours
6-8 hours 