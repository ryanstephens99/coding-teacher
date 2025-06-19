# Epic 2: Desktop Companion App - Core Service & IPC Server

## Overview
Create the FastAPI backend service that communicates with the plugin and hosts analysis logic.

## Goal
Build a robust Python-based companion application using FastAPI that can receive code snippets from the VS Code extension, process them, and return analysis results.

## Key Technologies
- Python 3.9+
- FastAPI
- WebSocket/IPC
- Pydantic
- Uvicorn
- AsyncIO

## Dependencies
- Requires Epic 1 (CM-T1.2) for IPC communication

## Estimated Effort
2-3 weeks

## Architecture Decisions
Based on modern FastAPI patterns and WebSocket best practices:
- Use FastAPI's native WebSocket support for real-time communication
- Implement async/await patterns for non-blocking I/O
- Use Pydantic models for data validation and serialization
- Structure as modular service with clear separation of concerns

## Tickets
1. [CM-T2.1: FastAPI Project Setup](./tickets/CM-T2.1.md) - Initialize Python project with FastAPI
2. [CM-T2.2: WebSocket IPC Server Setup](./tickets/CM-T2.2.md) - Implement WebSocket server for plugin communication
3. [CM-T2.3: Analysis Request Handler](./tickets/CM-T2.3.md) - Process incoming code analysis requests
4. [CM-T2.4: Health Check & Monitoring System](./tickets/CM-T2.4.md) - Service status and diagnostics
5. [CM-T2.5: Configuration Management & Environment Setup](./tickets/CM-T2.5.md) - Environment configuration and deployment setup
6. [CM-T2.6: Companion App Packaging & Distribution](./tickets/CM-T2.6.md) - Executable generation and distribution

## Success Criteria
- FastAPI server starts and runs stably
- WebSocket connections handled reliably with reconnection support
- Code snippets received and processed correctly
- Health monitoring and error handling implemented
- Application can be packaged and distributed 