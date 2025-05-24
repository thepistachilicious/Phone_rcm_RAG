# chatbot-backend/api/rag_route.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from rag.retriever import get_llama_response

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/rag/query")
async def ask_question(data: QueryRequest):
    try:
        result = get_llama_response(data.question)
        return {
            "answer": result["answer"],
            "is_retrieved": result["is_retrieved"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
