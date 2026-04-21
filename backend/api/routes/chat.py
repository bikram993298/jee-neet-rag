from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any
from backend.rag.retriever import retrieve_context
from backend.models.gemini_llm import generate_answer
from backend.utils.query_rewriter import rewrite_followup_question
from backend.utils.auth import get_current_user

router = APIRouter()


class ChatRequest(BaseModel):
    messages: list[dict]  # Expect full chat history


@router.post("/chat")
async def chat(
    req: ChatRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    history = req.messages

    # 🧩 Safety check
    if not history or not history[-1].get("text", "").strip():
        raise HTTPException(status_code=400, detail="Empty user message.")

    print(f"\n📩 Incoming Request — Total messages: {len(history)}")

    # 🧠 Step 1: Rephrase follow-ups (“explain more”, “in details”) into standalone queries
    rewritten_query = rewrite_followup_question(history)
    print(f"🧠 Rewritten Query: {rewritten_query}")

    # 📚 Step 2: Retrieve NCERT context using RAG
    context = retrieve_context(rewritten_query, k=7)
    context_preview = (context[:250] + "...") if len(context) > 250 else context
    print(f"📖 Context snippet: {context_preview}")

    # 🧮 Step 3: Build structured prompt for Gemini
    prompt = f"""You are a precise, formal JEE/NEET tutor (Physics). Follow these rules exactly:

1. **Output format (required)** — Return the entire answer in **Markdown** only.
   - Use `###` for headings.
   - Use bullet points for steps.
   - Use `**bold**` for final results.
   - Use inline math `\\( ... \\)` and display math `$$ ... $$` for equations.
   - Do **not** include code fences (```) or JSON. Only pure Markdown.

2. **Context use** — Reference NCERT context where applicable.
   - If the answer is directly in CONTEXT, mention it briefly and solve.
   - If not found, say:
     "This question is not directly covered in the provided NCERT context, but it can be solved using related NCERT concepts:"
     Then proceed logically using those concepts.

3. **Solution structure:**
   - **Plan** – 1–2 lines summary.
   - **Solution** – numbered, step-by-step with formulas and reasoning.
   - **Final Answer** – clearly boxed or bolded.

4. **Tone:** Academic and exam-focused (JEE/NEET). No motivational or irrelevant content.

5. **Formatting Example:**

### Plan
- Apply conservation of angular momentum.

### Solution
1. $$I_i \\omega_i = I_f \\omega_f$$  
2. $$\\omega_f = \\dfrac{{I_i}}{{I_f}}\\omega_i = \\dfrac{{5}}{{2}}\\omega_i$$

### Final Answer:
**\\(K_f/K_i = 5/4\\)**

---

CONTEXT:
{context}

QUESTION:
{rewritten_query}

Answer (Markdown + LaTeX only):
"""

    # ⚙️ Step 4: Generate answer using Gemini
    try:
        answer = generate_answer(prompt)
        if not answer or not answer.strip():
            raise RuntimeError("Empty answer returned from Gemini model.")
        print("✅ Answer generated successfully!")
    except Exception as e:
        print(f"❌ generate_answer exception: {e}")
        answer = f"[Gemini Error] {e}"

    # ✅ Step 5: Return answer
    return {"answer": answer}
