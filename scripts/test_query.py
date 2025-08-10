import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load FAISS index and embedding model
INDEX_PATH = "data/embeddings/ncert_jee_neet.index"
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
index = faiss.read_index(INDEX_PATH)

def search(query, top_k=3):
    q_emb = model.encode([query])
    distances, ids = index.search(np.array(q_emb, dtype="float32"), top_k)
    return ids[0], distances[0]

if __name__ == "__main__":
    while True:
        query = input("\nEnter your query (or 'exit'): ")
        if query.lower() == "exit":
            break
        ids, dists = search(query)
        print(f"Top {len(ids)} matches: {ids} (distances: {dists})")
