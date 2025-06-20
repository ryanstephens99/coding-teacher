"""
LLM API routes for Q&A functionality
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()

# Request/Response models
class QuestionRequest(BaseModel):
    question: str
    context: Optional[dict] = None

class QuestionResponse(BaseModel):
    answer: str
    confidence: float
    sources: Optional[List[str]] = None

@router.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question about coding conventions or practices
    """
    # TODO: Implement actual LLM integration
    # For now, return a mock response
    return QuestionResponse(
        answer="This is a placeholder response. LLM integration will be implemented here.",
        confidence=0.8,
        sources=["MDN Web Docs", "TypeScript Handbook"]
    )

@router.post("/explain")
async def explain_violation(violation_id: str):
    """
    Get detailed explanation for a specific convention violation
    """
    # TODO: Implement violation explanation logic
    return {
        "violation_id": violation_id,
        "explanation": "Detailed explanation will be generated here.",
        "examples": [
            {
                "title": "Good Example",
                "code": "const userName = 'john';",
                "explanation": "Uses camelCase naming convention"
            },
            {
                "title": "Bad Example", 
                "code": "const user_name = 'john';",
                "explanation": "Uses snake_case instead of camelCase"
            }
        ]
    }

@router.get("/examples/{rule_id}")
async def get_rule_examples(rule_id: str):
    """
    Get code examples for a specific rule
    """
    # TODO: Implement rule example retrieval
    return {
        "rule_id": rule_id,
        "examples": [
            {
                "title": "Correct Usage",
                "code": "// Example code here",
                "explanation": "Why this is the correct approach"
            }
        ]
    } 