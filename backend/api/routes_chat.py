# backend/api/routes_chat.py
from fastapi import APIRouter
from pydantic import BaseModel
from backend.rag.chain import answer_question

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    mode: str = "explain"  # or "mcq"
    k: int = 3

class ChatResponse(BaseModel):
    answer: str

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    res = answer_question(req.question, k=req.k, mode=req.mode)
    return {"answer": res["answer"]}
