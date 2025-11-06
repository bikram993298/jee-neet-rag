from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.rag.retriever import retrieve_context
from backend.models.gemini_llm import generate_answer


router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def chat(req: ChatRequest):
    query = req.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Empty query")

    context = retrieve_context(query, k=5)

    prompt = (
        "You are a helpful, precise JEE/NEET tutor. Use the following context from NCERT and past papers. "
        "Answer step-by-step and show final result clearly. If the context does not answer the question, be honest.\n\n"
        f"CONTEXT:\n{context}\n\nQUESTION:\n{query}\n\nAnswer:"
    )

    answer = generate_answer(prompt)
    return {"answer": answer}
