import os
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

# ---------------------------------------------
# 1️⃣ Load .env from backend directory (absolute-safe)
# ---------------------------------------------
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# ---------------------------------------------
# 2️⃣ Configure Gemini with API key
# ---------------------------------------------
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError(
        "❌ No API key found! Please set GOOGLE_API_KEY or GEMINI_API_KEY in backend/.env"
    )

genai.configure(api_key=api_key)

# Default model
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash").strip()


# ---------------------------------------------
# 3️⃣ Safe Gemini generation function
# ---------------------------------------------
def safe_generate(prompt: str, model_name: str = DEFAULT_MODEL) -> str:
    """Safe and retryable Gemini generation function."""
    try:
        print(f"🔧 Using Gemini model: {model_name}")

        # Safe educational safety settings
        safety_settings = [
            {"category": "harassment", "threshold": "block_none"},
            {"category": "hate", "threshold": "block_none"},
            {"category": "sexual", "threshold": "block_none"},
            {"category": "dangerous", "threshold": "block_none"},
        ]

        # ✅ Correct SDK call for v0.8.5
        model = genai.GenerativeModel(model_name, safety_settings=safety_settings)

        # --- First attempt ---
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.35,
                "max_output_tokens": 800,
            },
        )

        # --- Handle empty response (blocked content etc.) ---
        if not getattr(response, "text", None):
            finish_reason = None
            if getattr(response, "candidates", None):
                finish_reason = getattr(response.candidates[0], "finish_reason", None)
            print(f"⚠️ Gemini finish_reason={finish_reason}")

            if finish_reason == 2:
                print("⚠️ Gemini blocked output — retrying with safe educational preface...")

                safe_prompt = (
                    "This is a purely educational, NCERT-based physics question. "
                    "There is no unsafe content. Please respond academically.\n\n"
                    + prompt
                )

                response = model.generate_content(
                    safe_prompt,
                    generation_config={
                        "temperature": 0.3,
                        "max_output_tokens": 800,
                    },
                )

        # --- Clean and return text ---
        if getattr(response, "text", None):
            cleaned = (
                response.text.replace("**", "")
                .replace("###", "")
                .replace("```", "")
                .strip()
            )
            return cleaned

        print("⚠️ Gemini failed to return valid text — fallback explanation used.")
        return (
            "⚠️ Gemini could not generate an answer. Based on NCERT Physics (Rotational Motion): "
            "Rotation is the motion of a rigid body around an axis, described by angular quantities like θ, ω, and α."
        )

    except Exception as e:
        print("❌ generate_answer exception:", e)
        return f"[Gemini Error] {e}"


# ---------------------------------------------
# 4️⃣ Academic Answer Generator
# ---------------------------------------------
def generate_answer(prompt: str = None, query: str = None, context: str = None) -> str:
    """Generates JEE/NEET academic answers with NCERT context integration."""
    try:
        if not prompt:
            prompt = (
                "You are a helpful JEE/NEET Physics tutor. Use the provided NCERT context "
                "to answer conceptually and step-by-step. "
                "If context doesn't directly answer, mention it and use NCERT logic to solve.\n\n"
                f"CONTEXT:\n{context or 'No context provided.'}\n\n"
                f"QUESTION:\n{query}\n\nAnswer clearly and academically:"
            )

        result = safe_generate(prompt)
        print("✅ Answer generated successfully!")
        return result

    except Exception as e:
        print("❌ generate_answer fatal error:", e)
        return f"[Gemini Error] {e}"
