from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from pathlib import Path
from backend.config import FAISS_INDEX_PATH, ID_MAP_PATH, EMBEDDING_MODEL

_model = None
_index = None
_id_map = None

def _load_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model

def _load_index():
    global _index
    if _index is None:
        if not Path(FAISS_INDEX_PATH).exists():
            raise FileNotFoundError(f"FAISS index not found at {FAISS_INDEX_PATH}. Run rag/ingest.py")
        _index = faiss.read_index(str(FAISS_INDEX_PATH))
    return _index

def _load_id_map():
    global _id_map
    if _id_map is None:
        with open(ID_MAP_PATH, 'rb') as f:
            _id_map = pickle.load(f)
    return _id_map

def retrieve_context(query: str, k: int = 5):
    model = _load_model()
    index = _load_index()
    id_map = _load_id_map()

    q_emb = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(q_emb.astype('float32'), k)
    results = []
    for idx in indices[0]:
        if int(idx) in id_map:
            results.append(id_map[int(idx)])
    return "\n\n".join(results)
