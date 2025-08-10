# backend/rag/retriever.py
import faiss
import numpy as np
import json
import os
from backend.config import settings
from backend.models.embeddings import embed_texts

class SimpleFaissRetriever:
    def __init__(self, index_path=None, meta_path=None):
        index_path = index_path or os.path.join(settings.faiss_index_dir, "jee_neet.index")
        meta_path = meta_path or os.path.join(settings.faiss_index_dir, "jee_neet_meta.jsonl")
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"Faiss index not found: {index_path}")
        self.index = faiss.read_index(index_path)
        # load metadata
        self.meta = []
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                for line in f:
                    self.meta.append(json.loads(line))
        else:
            self.meta = []

    def retrieve(self, query, k=4):
        vec = embed_texts([query])[0].astype("float32")
        D, I = self.index.search(np.array([vec]), k)
        results = []
        for idx in I[0]:
            if idx < len(self.meta):
                results.append(self.meta[idx])
            else:
                results.append({"meta": {"source": "unknown"}, "text": ""})
        return results
