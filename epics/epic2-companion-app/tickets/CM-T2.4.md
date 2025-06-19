# CM-T2.4: Basic Service Health Check

## Summary
Implement basic health check endpoints and service monitoring for the companion app.

## Acceptance Criteria
- [ ] Health check endpoints for service status
- [ ] Application metrics collection and reporting
- [ ] Logging infrastructure with structured output
- [ ] Performance monitoring and alerting
- [ ] Database and external service health checks
- [ ] Graceful shutdown and startup procedures

## Implementation Details

### Health Check Service (app/services/health_service.py)
```python
"""
Health monitoring and diagnostics service for the companion app.
Provides comprehensive health checks and system metrics.
"""
import asyncio
import logging
import psutil
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.services.websocket_manager import websocket_manager
from app.services.analysis_service import analysis_service

logger = logging.getLogger(__name__)

class HealthStatus(BaseModel):
    """Health status for a component"""
    status: str  # 'healthy', 'degraded', 'unhealthy'
    message: Optional[str] = None
    last_check: datetime
    response_time_ms: Optional[float] = None

class SystemMetrics(BaseModel):
    """System performance metrics"""
    cpu_usage_percent: float
    memory_usage_percent: float
    memory_available_mb: float
    disk_usage_percent: float
    uptime_seconds: float

class ServiceHealth(BaseModel):
    """Overall service health status"""
    overall_status: str
    components: Dict[str, HealthStatus]
    metrics: SystemMetrics
    timestamp: datetime

class HealthService:
    """Service for monitoring application health and performance"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.health_checks: Dict[str, HealthStatus] = {}
        self.check_intervals = {
            'websocket': 30,  # seconds
            'analysis': 30,
            'system': 10,
            'memory': 60
        }
        
        # Start background health monitoring
        self._start_health_monitoring()

    def _start_health_monitoring(self):
        """Start background health check tasks"""
        asyncio.create_task(self._periodic_health_checks())
        asyncio.create_task(self._system_monitoring())

    async def _periodic_health_checks(self):
        """Run periodic health checks for all components"""
        while True:
            try:
                # Check WebSocket manager
                await self._check_websocket_health()
                
                # Check analysis service
                await self._check_analysis_health()
                
                # Sleep between checks
                await asyncio.sleep(30)
                
            except Exception as e:
                logger.error(f"Error in periodic health checks: {e}")
                await asyncio.sleep(60)  # Back off on error

    async def _system_monitoring(self):
        """Monitor system resources continuously"""
        while True:
            try:
                await self._check_system_health()
                await asyncio.sleep(self.check_intervals['system'])
                
            except Exception as e:
                logger.error(f"Error in system monitoring: {e}")
                await asyncio.sleep(30)

    async def _check_websocket_health(self):
        """Check WebSocket manager health"""
        start_time = time.time()
        
        try:
            # Get connection stats
            stats = websocket_manager.get_connection_stats()
            
            # Determine health based on stats
            if stats['total_connections'] >= 0:  # Basic connectivity check
                status = 'healthy'
                message = f"Active connections: {stats['total_connections']}"
            else:
                status = 'unhealthy'
                message = "WebSocket manager not responding"
            
            response_time = (time.time() - start_time) * 1000
            
            self.health_checks['websocket'] = HealthStatus(
                status=status,
                message=message,
                last_check=datetime.now(),
                response_time_ms=response_time
            )
            
        except Exception as e:
            self.health_checks['websocket'] = HealthStatus(
                status='unhealthy',
                message=f"WebSocket check failed: {str(e)}",
                last_check=datetime.now(),
                response_time_ms=(time.time() - start_time) * 1000
            )

    async def _check_analysis_health(self):
        """Check analysis service health"""
        start_time = time.time()
        
        try:
            # Get analysis service stats
            stats = analysis_service.get_stats()
            
            # Determine health based on queue and active requests
            queue_size = stats.get('queue_size', 0)
            active_requests = stats.get('active_requests', 0)
            
            if queue_size < 100 and active_requests >= 0:
                status = 'healthy'
                message = f"Queue: {queue_size}, Active: {active_requests}"
            elif queue_size < 500:
                status = 'degraded'
                message = f"High queue size: {queue_size}"
            else:
                status = 'unhealthy'
                message = f"Queue overloaded: {queue_size}"
            
            response_time = (time.time() - start_time) * 1000
            
            self.health_checks['analysis'] = HealthStatus(
                status=status,
                message=message,
                last_check=datetime.now(),
                response_time_ms=response_time
            )
            
        except Exception as e:
            self.health_checks['analysis'] = HealthStatus(
                status='unhealthy',
                message=f"Analysis check failed: {str(e)}",
                last_check=datetime.now(),
                response_time_ms=(time.time() - start_time) * 1000
            )

    async def _check_system_health(self):
        """Check system resource health"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available_mb = memory.available / 1024 / 1024
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # Determine overall system health
            if cpu_percent < 80 and memory_percent < 85 and disk_percent < 90:
                status = 'healthy'
                message = f"CPU: {cpu_percent:.1f}%, Memory: {memory_percent:.1f}%, Disk: {disk_percent:.1f}%"
            elif cpu_percent < 90 and memory_percent < 95 and disk_percent < 95:
                status = 'degraded'
                message = f"High resource usage - CPU: {cpu_percent:.1f}%, Memory: {memory_percent:.1f}%"
            else:
                status = 'unhealthy'
                message = f"Critical resource usage - CPU: {cpu_percent:.1f}%, Memory: {memory_percent:.1f}%"
            
            self.health_checks['system'] = HealthStatus(
                status=status,
                message=message,
                last_check=datetime.now()
            )
            
        except Exception as e:
            self.health_checks['system'] = HealthStatus(
                status='unhealthy',
                message=f"System check failed: {str(e)}",
                last_check=datetime.now()
            )

    def get_system_metrics(self) -> SystemMetrics:
        """Get current system metrics"""
        try:
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            uptime = (datetime.now() - self.start_time).total_seconds()
            
            return SystemMetrics(
                cpu_usage_percent=cpu_percent,
                memory_usage_percent=memory.percent,
                memory_available_mb=memory.available / 1024 / 1024,
                disk_usage_percent=disk.percent,
                uptime_seconds=uptime
            )
            
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return SystemMetrics(
                cpu_usage_percent=0.0,
                memory_usage_percent=0.0,
                memory_available_mb=0.0,
                disk_usage_percent=0.0,
                uptime_seconds=0.0
            )

    def get_service_health(self) -> ServiceHealth:
        """Get overall service health"""
        # Determine overall status
        statuses = [check.status for check in self.health_checks.values()]
        
        if not statuses:
            overall_status = 'unknown'
        elif all(status == 'healthy' for status in statuses):
            overall_status = 'healthy'
        elif any(status == 'unhealthy' for status in statuses):
            overall_status = 'unhealthy'
        else:
            overall_status = 'degraded'
        
        return ServiceHealth(
            overall_status=overall_status,
            components=self.health_checks.copy(),
            metrics=self.get_system_metrics(),
            timestamp=datetime.now()
        )

    def is_healthy(self) -> bool:
        """Quick health check for simple true/false status"""
        return self.get_service_health().overall_status in ['healthy', 'degraded']

    def get_uptime(self) -> timedelta:
        """Get service uptime"""
        return datetime.now() - self.start_time

# Global instance
health_service = HealthService()
```

### Health Check Router (app/routers/health.py)
```python
"""
Health check and monitoring API endpoints.
"""
from fastapi import APIRouter, Response, status
from app.services.health_service import health_service

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check endpoint"""
    service_health = health_service.get_service_health()
    
    if service_health.overall_status == 'healthy':
        return {"status": "healthy", "timestamp": service_health.timestamp}
    elif service_health.overall_status == 'degraded':
        return {"status": "degraded", "timestamp": service_health.timestamp}
    else:
        return Response(
            content='{"status": "unhealthy"}', 
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            media_type="application/json"
        )

@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with component status"""
    return health_service.get_service_health()

@router.get("/health/components")
async def component_health():
    """Get health status of individual components"""
    service_health = health_service.get_service_health()
    return service_health.components

@router.get("/metrics")
async def system_metrics():
    """Get system performance metrics"""
    return health_service.get_system_metrics()

@router.get("/metrics/uptime")
async def uptime():
    """Get service uptime"""
    uptime = health_service.get_uptime()
    return {
        "uptime_seconds": uptime.total_seconds(),
        "uptime_string": str(uptime),
        "started_at": health_service.start_time
    }

@router.get("/ping")
async def ping():
    """Simple ping endpoint for load balancers"""
    return {"status": "pong", "timestamp": datetime.now()}
```

### Logging Configuration (app/core/logging.py)
```python
"""
Centralized logging configuration for the application.
"""
import logging
import logging.config
import sys
from datetime import datetime

def setup_logging(level: str = "INFO", json_format: bool = False):
    """
    Setup application logging with structured output.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        json_format: Whether to use JSON formatted logs
    """
    
    if json_format:
        # JSON formatter for production
        formatter_config = {
            'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s", "module": "%(module)s", "function": "%(funcName)s", "line": %(lineno)d}'
        }
    else:
        # Human-readable formatter for development
        formatter_config = {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }

    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': formatter_config,
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': sys.stdout,
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': 'logs/companion_app.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
            },
        },
        'loggers': {
            '': {  # Root logger
                'level': level,
                'handlers': ['console', 'file'],
                'propagate': False,
            },
            'uvicorn': {
                'level': 'INFO',
                'handlers': ['console', 'file'],
                'propagate': False,
            },
            'fastapi': {
                'level': 'INFO',
                'handlers': ['console', 'file'],
                'propagate': False,
            },
        },
    }

    # Create logs directory if it doesn't exist
    import os
    os.makedirs('logs', exist_ok=True)
    
    logging.config.dictConfig(logging_config)
    
    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized - Level: {level}, JSON Format: {json_format}")
```

### Application Lifecycle (app/core/lifecycle.py)
```python
"""
Application lifecycle management for graceful startup and shutdown.
"""
import asyncio
import signal
import logging
from typing import List, Callable

logger = logging.getLogger(__name__)

class LifecycleManager:
    """Manages application startup and shutdown procedures"""
    
    def __init__(self):
        self.startup_tasks: List[Callable] = []
        self.shutdown_tasks: List[Callable] = []
        self._shutdown_event = asyncio.Event()

    def add_startup_task(self, task: Callable):
        """Add a task to run during startup"""
        self.startup_tasks.append(task)

    def add_shutdown_task(self, task: Callable):
        """Add a task to run during shutdown"""
        self.shutdown_tasks.append(task)

    async def startup(self):
        """Execute all startup tasks"""
        logger.info("Starting application lifecycle tasks...")
        
        for task in self.startup_tasks:
            try:
                if asyncio.iscoroutinefunction(task):
                    await task()
                else:
                    task()
                logger.info(f"Startup task completed: {task.__name__}")
            except Exception as e:
                logger.error(f"Startup task failed: {task.__name__} - {e}")
                raise

        logger.info("All startup tasks completed successfully")

    async def shutdown(self):
        """Execute all shutdown tasks"""
        logger.info("Starting graceful shutdown...")
        
        for task in reversed(self.shutdown_tasks):  # Reverse order for cleanup
            try:
                if asyncio.iscoroutinefunction(task):
                    await task()
                else:
                    task()
                logger.info(f"Shutdown task completed: {task.__name__}")
            except Exception as e:
                logger.error(f"Shutdown task failed: {task.__name__} - {e}")

        logger.info("Graceful shutdown completed")

    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, initiating graceful shutdown...")
            self._shutdown_event.set()

        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

    async def wait_for_shutdown(self):
        """Wait for shutdown signal"""
        await self._shutdown_event.wait()

# Global instance
lifecycle_manager = LifecycleManager()
```

### Main App Integration (app/main.py updates)
```python
from app.routers import health
from app.services.health_service import health_service
from app.core.logging import setup_logging
from app.core.lifecycle import lifecycle_manager

# Setup logging
setup_logging(level="INFO", json_format=False)  # Set to True for production

# Include health router
app.include_router(health.router, prefix="/api/v1", tags=["health"])

@app.on_event("startup")
async def startup_event():
    """Application startup"""
    logger.info("CodeMentor Companion App starting up...")
    
    # Execute lifecycle startup tasks
    await lifecycle_manager.startup()
    
    logger.info("Health monitoring service initialized")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    logger.info("CodeMentor Companion App shutting down...")
    
    # Execute lifecycle shutdown tasks
    await lifecycle_manager.shutdown()
```

## Technical Notes
- Implements comprehensive health monitoring for all components
- Provides both simple and detailed health check endpoints
- Includes system resource monitoring with thresholds
- Uses structured logging for better observability
- Implements graceful startup and shutdown procedures
- Follows production-ready monitoring patterns

## Dependencies
- FastAPI project setup from CM-T2.1
- WebSocket manager from CM-T2.2
- Analysis service from CM-T2.3
- psutil for system monitoring

## Testing
- Health check endpoints return correct status codes
- Component health checks work correctly
- System metrics are accurate
- Graceful shutdown procedures work
- Logging output is structured and useful

## Estimated Hours
6-8 hours 