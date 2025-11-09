import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))

def rewrite_followup_question(history: list[dict], model_name="gemini-2.0-flash"):
    """
    Rewrites user's latest question into a standalone academic query.
    Useful when user says vague things like 'in details' or 'explain more'.
    """

    if not history:
        return ""

    last_user = history[-1]["text"].strip().lower()

    # Detect vague or incomplete follow-ups
    vague_triggers = [
        "in detail", "in details", "tell me more", "discuss", "discuss more",
        "explain more", "elaborate", "continue", "go on", "more", "in detilsa", "expand", "explain it"
    ]

    # 🧠 If user just said “in details” or similar → use last meaningful user question
    if any(v in last_user for v in vague_triggers):
        for msg in reversed(history[:-1]):
            if msg["role"] == "user":
                prev_q = msg["text"].strip()
                return f"Explain in more detail about: {prev_q}"
        return "Explain in more detail about the previous topic."

    # 🧠 Otherwise, let Gemini rewrite properly
    chat_history = [
        {"role": msg.get("role", "user"), "parts": [msg.get("text", "")]}
        for msg in history
    ]

    # System instruction for rewriting
    system_instruction = (
        "You are a query rewriting expert. "
        "Based on the provided chat history, rephrase the last user question "
        "into a complete, standalone academic question that can be understood "
        "without chat context. "
        "Output only the rewritten question text and nothing else."
    )

    # Combine context + history
    contents = [
    {"role": "user", "parts": [system_instruction + "\n\n" + history[-1]["text"]]}
]


    # Create Gemini model with v0.8.5-safe syntax
    model = genai.GenerativeModel(
        model_name,
           safety_settings=[
        {"category": "harassment", "threshold": "block_none"},
        {"category": "hate", "threshold": "block_none"},
        {"category": "sexual", "threshold": "block_none"},
        {"category": "dangerous", "threshold": "block_none"},
    ],

    )

    try:
        response = model.generate_content(
            contents=contents,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 100,
            },
        )

        rewritten = getattr(response, "text", "").strip()
        if rewritten:
            return rewritten
        return history[-1]["text"]

    except Exception as e:
        print("⚠️ Query Rewriter Error:", e)
        return history[-1]["text"]
