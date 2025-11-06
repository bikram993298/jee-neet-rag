import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from tqdm import tqdm

BASE = Path(__file__).resolve().parents[2]  # Go up one more level to reach project root
DATA_DIR = BASE / "data"
NCERT_DIR = DATA_DIR / "ncert"
EMBED_DIR = DATA_DIR / "embeddings"
EMBED_DIR.mkdir(parents=True, exist_ok=True)
INDEX_PATH = EMBED_DIR / "faiss_index.idx"
ID_MAP_PATH = EMBED_DIR / "id_to_text.pkl"
MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

CHUNK_SIZE = 450
CHUNK_OVERLAP = 120

model = SentenceTransformer(MODEL_NAME)

def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    parts = []
    start = 0
    while start < len(text):
        end = start + size
        parts.append(text[start:end].strip())
        start = max(0, end - overlap)
    return [p for p in parts if p]

if __name__ == "__main__":
    print(f"Looking for text files in: {NCERT_DIR}")
    texts = []
    ids = []
    file_paths = list(NCERT_DIR.glob("*.txt"))
    print(f"Found files: {[f.name for f in file_paths]}")
    idx_counter = 0

    for fp in file_paths:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        chunks = chunk_text(content)
        for c in chunks:
            texts.append(c)
            ids.append(idx_counter)
            idx_counter += 1

    if not texts:
        print("No text files found in data/ncert/. Add .txt files first.")
        exit(1)

    print(f"Embedding {len(texts)} chunks with {MODEL_NAME} ...")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    dim = embeddings.shape[1]

    print("Building FAISS index...")
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings.astype('float32'))

    print(f"Saving index -> {INDEX_PATH}")
    faiss.write_index(index, str(INDEX_PATH))

    print(f"Saving id->text map -> {ID_MAP_PATH}")
    id_to_text = {i: t for i, t in zip(ids, texts)}
    with open(ID_MAP_PATH, 'wb') as f:
        pickle.dump(id_to_text, f)

    print("Done.")
