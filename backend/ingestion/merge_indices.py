# backend/ingestion/merge_indices.py
import faiss
import os
import numpy as np
from backend.config import settings

def merge_indexes(index_paths, out_path):
    # loads IndexFlatL2 indexes and concatenates their vectors
    vectors = []
    metas = []
    dims = None
    for p in index_paths:
        idx = faiss.read_index(p)
        xb = faiss.vector_to_array(idx.xb) if hasattr(idx, "xb") else None
        # easier approach: read metadata files and re-embed? For simplicity assume same dim and IndexFlatL2
        # Faiss does not offer a standard API to extract all vectors across all Index types reliably.
        # A robust production approach: keep saved numpy embeddings per source. For brevity, we will instruct user to re-create unified index by concatenating saved embeddings.
        pass

    # NOTE: For now, you should rebuild merged index from combined embeddings saved during ingestion.
    raise NotImplementedError("Merging raw faiss indexes is brittle; rebuild merged index from saved embeddings or use the `merge_embeddings.py` helper.")
