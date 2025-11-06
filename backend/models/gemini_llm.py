import os
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

# Ensure we load the backend/.env even if the process cwd is the repo root.
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Prefer the expected GOOGLE_API_KEY environment variable used by the library,
# but fall back to GEMINI_API_KEY if present (for backward compatibility).
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError(
        "No API key found for Gemini. Set the GOOGLE_API_KEY (preferred) or GEMINI_API_KEY "
        "environment variable, or configure Application Default Credentials (ADC)."
    )

genai.configure(api_key=api_key)

def _discover_model_name():
    """Return the model name to use.

    Priority:
    1. GEMINI_MODEL env var
    2. If not set, attempt to list available models and return None (user must set GEMINI_MODEL)
    """
    model_name = os.getenv("GEMINI_MODEL")
    if model_name:
        return model_name

    # Attempt to list models to provide a helpful message (best-effort). Don't fail the import
    try:
        models = genai.list_models()
        names = []
        # models may be a sequence or an object; attempt several access patterns
        if isinstance(models, dict):
            candidates = models.get("models") or models.get("model") or []
        else:
            candidates = models
        for m in candidates:
            if isinstance(m, str):
                names.append(m)
            else:
                nm = getattr(m, "name", None) or getattr(m, "model", None)
                if not nm and isinstance(m, dict):
                    nm = m.get("name") or m.get("model")
                if nm:
                    names.append(nm)
        preview = ", ".join(names[:10]) if names else "<no models returned>"
        raise RuntimeError(
            "No GEMINI_MODEL set. Please set the GEMINI_MODEL environment variable to one of the available models: "
            f"{preview}"
        )
    except Exception:
        # If listing failed, instruct the user to set GEMINI_MODEL explicitly.
        raise RuntimeError(
            "No GEMINI_MODEL environment variable set. Please set GEMINI_MODEL to a supported model name "
            "(for example, check the Google Generative AI docs or call genai.list_models() manually)."
        )


def generate_answer(prompt: str):
    try:
        model_name = _discover_model_name()
        # _discover_model_name will raise if no model_name could be determined
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # If this is a model-not-found error, surface a clearer message to the caller.
        err = str(e)
        if "404" in err or "not found" in err.lower():
            return (
                f"[Gemini Error] Model '{os.getenv('GEMINI_MODEL') or '<not set>'}' not found or not supported. "
                "Set the GEMINI_MODEL env var to a supported model (see available models via genai.list_models())."
            )
        return f"[Gemini Error] {e}"
