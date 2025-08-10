# backend/models/embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np
from backend.config import settings

_model = None

def get_embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.embedding_model, device=settings.device)
    return _model

def embed_texts(texts):
    model = get_embedding_model()
    embeddings = model.encode(list(texts), show_progress_bar=False, convert_to_numpy=True)
    return embeddings  # numpy array
