"""
Pytest configuration and fixtures for companion app testing
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src.main import app


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
async def async_client():
    """Create an async test client for the FastAPI app."""
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client


@pytest.fixture
def sample_analysis_request():
    """Sample analysis request for testing."""
    return {
        "language": "typescript",
        "code": "const userName = 'john';",
        "fileName": "test.ts"
    }


@pytest.fixture
def sample_question_request():
    """Sample question request for testing."""
    return {
        "question": "Why should I use camelCase?",
        "context": {
            "language": "typescript",
            "code": "const user_name = 'john';"
        }
    }


@pytest.fixture
def mock_violation():
    """Sample convention violation for testing."""
    return {
        "id": "test-violation-1",
        "rule": "naming-convention",
        "severity": "warning",
        "message": "Variable should use camelCase",
        "line": 1,
        "column": 6,
        "suggestion": "Use camelCase naming convention",
        "reasoning": "camelCase improves readability"
    } 