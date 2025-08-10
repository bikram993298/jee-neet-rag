# backend/rag/chain.py
from backend.rag.retriever import SimpleFaissRetriever
from backend.rag.prompt_templates import MCQ_PROMPT, EXPLAIN_PROMPT
from backend.models.hybrid_router import hybrid_generate

def build_context(retrieved):
    parts = []
    for r in retrieved:
        meta = r.get("meta", {})
        txt = r.get("text", "")
        src = meta.get("exam") or meta.get("source") or "unknown"
        parts.append(f"Source: {src}\n{txt}")
    return "\n\n---\n\n".join(parts)

def answer_question(question, k=3, mode="explain"):
    retriever = SimpleFaissRetriever()
    retrieved = retriever.retrieve(question, k=k)
    context = build_context(retrieved)
    if mode == "mcq":
        prompt = MCQ_PROMPT.format(context=context, question=question)
    else:
        prompt = EXPLAIN_PROMPT.format(context=context, question=question)
    resp = hybrid_generate(prompt)
    return {"answer": resp, "retrieved": retrieved}
