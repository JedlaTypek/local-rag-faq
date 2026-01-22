from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from app.rag.engine import RAGEngine

router = APIRouter()

class AskRequest(BaseModel):
    query: str

class AskResponse(BaseModel):
    query: str
    answer: str
    context: list

@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    try:
        engine = RAGEngine()
        result = engine.ask(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
