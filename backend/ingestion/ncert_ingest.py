# backend/ingestion/ncert_ingest.py
import os
from pathlib import Path
from backend.models.embeddings import embed_texts
import faiss
import numpy as np
import json
from backend.config import settings
from tqdm import tqdm

def chunk_text(text, chunk_size=800, overlap=100):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def ingest_ncert_from_folder(folder_path: str, out_dir=settings.faiss_index_dir):
    texts = []
    metadatas = []
    for path in Path(folder_path).rglob("*.txt"):
        content = path.read_text(encoding="utf-8")
        chunks = chunk_text(content)
        for idx, c in enumerate(chunks):
            texts.append(c)
            metadatas.append({"source": str(path), "chunk_idx": idx})

    embeddings = embed_texts(texts)
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(np.array(embeddings).astype("float32"))
    os.makedirs(out_dir, exist_ok=True)
    faiss.write_index(index, os.path.join(out_dir, "ncert.index"))

    with open(os.path.join(out_dir, "ncert_meta.jsonl"), "w", encoding="utf-8") as f:
        for meta, text in zip(metadatas, texts):
            f.write(json.dumps({"meta": meta, "text": text}) + "\n")
    print("NCERT ingestion finished.")
