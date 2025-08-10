# backend/models/local_llm.py
"""
Wrapper for a local model (Ollama/GPT4All). This is a simple abstraction so the rest of
the code calls `predict` uniformly.
"""
import requests
from backend.config import settings
import os
import json
from typing import Optional

class OllamaClient:
    def __init__(self, model_name="mistral"):
        self.model = model_name
        self.base = f"http://{settings.ollama_host}:{settings.ollama_port}"

    def predict(self, prompt: str, max_tokens: int = 512):
        # Minimal Ollama HTTP API call (adjust per your local runtime)
        url = f"{self.base}/api/generate"
        payload = {"model": self.model, "prompt": prompt, "max_tokens": max_tokens}
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json().get("text", "")

# If you use another runtime, implement a similar client class and swap here.
