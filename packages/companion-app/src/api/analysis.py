"""
Analysis API routes for code convention checking
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# Request/Response models
class AnalysisRequest(BaseModel):
    language: str
    code: str
    fileName: Optional[str] = None
    framework: Optional[str] = None

class ConventionViolation(BaseModel):
    id: str
    rule: str
    severity: str  # 'error' | 'warning' | 'info'
    message: str
    line: int
    column: int
    endLine: Optional[int] = None
    endColumn: Optional[int] = None
    suggestion: Optional[str] = None
    reasoning: Optional[str] = None

class AnalysisResponse(BaseModel):
    violations: List[ConventionViolation]
    analysisTime: float
    language: str

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_code(request: AnalysisRequest):
    """
    Analyze code for convention violations
    """
    # TODO: Implement actual code analysis logic
    # For now, return a mock response
    return AnalysisResponse(
        violations=[],
        analysisTime=0.1,
        language=request.language
    )

@router.get("/supported-languages")
async def get_supported_languages():
    """
    Get list of supported programming languages
    """
    return {
        "languages": [
            "typescript",
            "javascript", 
            "python",
            "java",
            "go",
            "rust",
            "c",
            "cpp"
        ]
    }

@router.get("/rules/{language}")
async def get_language_rules(language: str):
    """
    Get available convention rules for a specific language
    """
    if language not in ["typescript", "javascript", "python"]:
        raise HTTPException(status_code=404, detail="Language not supported")
    
    # TODO: Return actual rules from convention engine
    return {
        "language": language,
        "rules": [
            {
                "id": "naming-convention",
                "name": "Naming Convention",
                "description": "Variables should use camelCase",
                "severity": "warning"
            }
        ]
    } 