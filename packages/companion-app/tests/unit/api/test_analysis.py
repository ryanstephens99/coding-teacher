"""
Unit tests for analysis API routes
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_analyze_code_endpoint(client: TestClient, sample_analysis_request):
    """Test the code analysis endpoint."""
    response = client.post("/api/analysis/analyze", json=sample_analysis_request)
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "violations" in data
    assert "analyzed_lines" in data
    assert "language" in data
    assert "file_name" in data
    
    # Verify data types
    assert isinstance(data["violations"], list)
    assert isinstance(data["analyzed_lines"], int)
    assert data["language"] == sample_analysis_request["language"]
    assert data["file_name"] == sample_analysis_request["fileName"]


@pytest.mark.unit
def test_analyze_code_with_invalid_language(client: TestClient):
    """Test analysis with unsupported language."""
    invalid_request = {
        "language": "unsupported-language",
        "code": "some code",
        "fileName": "test.xyz"
    }
    
    response = client.post("/api/analysis/analyze", json=invalid_request)
    
    assert response.status_code == 200
    data = response.json()
    
    # Should still return valid response but with no violations
    assert "violations" in data
    assert isinstance(data["violations"], list)


@pytest.mark.unit
def test_analyze_code_with_empty_code(client: TestClient):
    """Test analysis with empty code."""
    empty_request = {
        "language": "typescript",
        "code": "",
        "fileName": "empty.ts"
    }
    
    response = client.post("/api/analysis/analyze", json=empty_request)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["violations"] == []
    assert data["analyzed_lines"] == 0


@pytest.mark.unit
def test_analyze_code_missing_fields(client: TestClient):
    """Test analysis with missing required fields."""
    incomplete_request = {
        "language": "typescript"
        # Missing code and fileName
    }
    
    response = client.post("/api/analysis/analyze", json=incomplete_request)
    
    # Should return validation error
    assert response.status_code == 422


@pytest.mark.unit
def test_get_supported_languages(client: TestClient):
    """Test getting supported languages."""
    response = client.get("/api/analysis/supported-languages")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "languages" in data
    assert isinstance(data["languages"], list)
    
    # Should include common languages
    languages = data["languages"]
    assert any(lang["id"] == "typescript" for lang in languages)
    assert any(lang["id"] == "javascript" for lang in languages)
    assert any(lang["id"] == "python" for lang in languages)
    
    # Verify language structure
    for lang in languages:
        assert "id" in lang
        assert "name" in lang
        assert "extensions" in lang
        assert isinstance(lang["extensions"], list)


@pytest.mark.unit
def test_get_rules_for_language(client: TestClient):
    """Test getting rules for a specific language."""
    response = client.get("/api/analysis/rules/typescript")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "language" in data
    assert "rules" in data
    assert data["language"] == "typescript"
    assert isinstance(data["rules"], list)
    
    # Verify rule structure
    for rule in data["rules"]:
        assert "id" in rule
        assert "name" in rule
        assert "description" in rule
        assert "severity" in rule
        assert "category" in rule


@pytest.mark.unit
def test_get_rules_for_unsupported_language(client: TestClient):
    """Test getting rules for unsupported language."""
    response = client.get("/api/analysis/rules/unsupported-lang")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["language"] == "unsupported-lang"
    assert data["rules"] == []


@pytest.mark.unit
def test_analyze_code_with_violations(client: TestClient):
    """Test analysis that should return violations."""
    request_with_violations = {
        "language": "typescript",
        "code": "const user_name = 'john'; var count = 0;",
        "fileName": "violations.ts"
    }
    
    response = client.post("/api/analysis/analyze", json=request_with_violations)
    
    assert response.status_code == 200
    data = response.json()
    
    # Should find violations in the problematic code
    assert len(data["violations"]) > 0
    
    # Verify violation structure
    for violation in data["violations"]:
        assert "id" in violation
        assert "rule" in violation
        assert "severity" in violation
        assert "message" in violation
        assert "line" in violation
        assert "column" in violation 