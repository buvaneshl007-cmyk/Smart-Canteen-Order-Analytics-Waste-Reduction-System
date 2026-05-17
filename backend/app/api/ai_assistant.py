from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.schemas import AIQuery, AIResponse
from app.api.auth import get_current_owner, User
from app.services.ai_service import query_ai_assistant, analyze_query_locally
from app.core.config import settings

router = APIRouter(prefix="/ai", tags=["AI Assistant"])


@router.post("/query", response_model=AIResponse)
async def ask_ai_assistant(
    query_data: AIQuery,
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Ask AI assistant a question about analytics"""
    
    # query_ai_assistant handles both Gemini AI and local analysis fallback
    response_text = query_ai_assistant(query_data.query, db)
    
    return {
        "response": response_text,
        "data": None
    }
