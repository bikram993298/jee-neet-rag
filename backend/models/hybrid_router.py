# backend/models/hybrid_router.py
"""
Hybrid router: attempt local LLM first, fall back to OpenAI GPT-4 when needed.
Simple heuristic: short answers or explicit fallback signals trigger GPT-4.
"""
from backend.models.local_llm import OllamaClient
from backend.config import settings
import openai

openai.api_key = settings.openai_api_key

local_llm = OllamaClient(model_name="mistral")

def call_openai(prompt, max_tokens=512, temperature=0.0):
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature
    )
    return resp["choices"][0]["message"]["content"]

def hybrid_generate(prompt, prefer_local=True):
    try:
        if prefer_local:
            out = local_llm.predict(prompt)
            # heuristic: if model is too short or contains a fallback phrase, use GPT-4
            if out is None or len(out.strip()) < 40 or "I don't know" in out.lower():
                raise RuntimeError("Local model unsatisfactory; using fallback.")
            return out
        else:
            return call_openai(prompt)
    except Exception as e:
        # fallback to OpenAI
        return call_openai(prompt)
