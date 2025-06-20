"""
Unit tests for LLM API routes
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_ask_question_endpoint(client: TestClient, sample_question_request):
    """Test the LLM question answering endpoint."""
    response = client.post("/api/llm/ask", json=sample_question_request)
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "answer" in data
    assert "confidence" in data
    assert "sources" in data
    assert "reasoning" in data
    
    # Verify data types
    assert isinstance(data["answer"], str)
    assert isinstance(data["confidence"], float)
    assert isinstance(data["sources"], list)
    assert isinstance(data["reasoning"], str)
    
    # Answer should not be empty
    assert len(data["answer"]) > 0
    
    # Confidence should be between 0 and 1
    assert 0 <= data["confidence"] <= 1


@pytest.mark.unit
def test_ask_question_missing_question(client: TestClient):
    """Test question endpoint with missing question field."""
    incomplete_request = {
        "context": {
            "language": "typescript",
            "code": "const test = 'hello';"
        }
        # Missing question field
    }
    
    response = client.post("/api/llm/ask", json=incomplete_request)
    
    # Should return validation error
    assert response.status_code == 422


@pytest.mark.unit
def test_ask_question_empty_question(client: TestClient):
    """Test question endpoint with empty question."""
    empty_request = {
        "question": "",
        "context": {
            "language": "typescript",
            "code": "const test = 'hello';"
        }
    }
    
    response = client.post("/api/llm/ask", json=empty_request)
    
    assert response.status_code == 200
    data = response.json()
    
    # Should handle empty question gracefully
    assert "answer" in data
    assert len(data["answer"]) > 0


@pytest.mark.unit
def test_ask_question_without_context(client: TestClient):
    """Test question endpoint without context."""
    no_context_request = {
        "question": "What is camelCase naming convention?"
    }
    
    response = client.post("/api/llm/ask", json=no_context_request)
    
    assert response.status_code == 200
    data = response.json()
    
    assert "answer" in data
    assert len(data["answer"]) > 0


@pytest.mark.unit
def test_explain_violation_endpoint(client: TestClient, mock_violation):
    """Test the violation explanation endpoint.""" 
    response = client.post("/api/llm/explain", json=mock_violation)
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "explanation" in data
    assert "suggestion" in data
    assert "examples" in data
    assert "reasoning" in data
    
    # Verify data types
    assert isinstance(data["explanation"], str)
    assert isinstance(data["suggestion"], str)
    assert isinstance(data["examples"], list)
    assert isinstance(data["reasoning"], str)
    
    # Content should not be empty
    assert len(data["explanation"]) > 0
    assert len(data["suggestion"]) > 0


@pytest.mark.unit
def test_explain_violation_missing_fields(client: TestClient):
    """Test violation explanation with missing fields."""
    incomplete_violation = {
        "rule": "naming-convention"
        # Missing other required fields
    }
    
    response = client.post("/api/llm/explain", json=incomplete_violation)
    
    # Should return validation error
    assert response.status_code == 422


@pytest.mark.unit
def test_get_rule_examples_endpoint(client: TestClient):
    """Test getting examples for a specific rule."""
    rule_id = "naming-convention"
    response = client.get(f"/api/llm/examples/{rule_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "rule_id" in data
    assert "examples" in data
    assert "description" in data
    
    assert data["rule_id"] == rule_id
    assert isinstance(data["examples"], list)
    assert isinstance(data["description"], str)
    
    # Should have examples
    assert len(data["examples"]) > 0
    
    # Verify example structure
    for example in data["examples"]:
        assert "title" in example
        assert "good" in example
        assert "bad" in example
        assert "explanation" in example


@pytest.mark.unit
def test_get_rule_examples_nonexistent_rule(client: TestClient):
    """Test getting examples for non-existent rule."""
    rule_id = "non-existent-rule"
    response = client.get(f"/api/llm/examples/{rule_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["rule_id"] == rule_id
    assert data["examples"] == []
    assert len(data["description"]) > 0  # Should still provide description


@pytest.mark.unit
def test_ask_complex_question(client: TestClient):
    """Test asking a complex coding question."""
    complex_request = {
        "question": "Why should I avoid using 'var' in TypeScript and JavaScript?",
        "context": {
            "language": "typescript",
            "code": "var count = 0; for (var i = 0; i < 10; i++) { var count = i; }"
        }
    }
    
    response = client.post("/api/llm/ask", json=complex_request)
    
    assert response.status_code == 200
    data = response.json()
    
    # Should provide detailed answer for complex question
    assert len(data["answer"]) > 100  # Expect detailed response
    assert data["confidence"] > 0.5  # Should be confident about basic concepts


@pytest.mark.unit
def test_explain_high_severity_violation(client: TestClient):
    """Test explaining a high severity violation."""
    high_severity_violation = {
        "id": "security-violation",
        "rule": "no-eval",
        "severity": "error",
        "message": "Use of eval() is not allowed",
        "line": 5,
        "column": 10,
        "suggestion": "Use safer alternatives to eval()",
        "reasoning": "eval() can execute arbitrary code"
    }
    
    response = client.post("/api/llm/explain", json=high_severity_violation)
    
    assert response.status_code == 200
    data = response.json()
    
    # Should provide detailed explanation for high severity issues
    assert len(data["explanation"]) > 50
    assert len(data["examples"]) > 0 