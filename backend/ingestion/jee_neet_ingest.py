# backend/ingestion/jee_neet_ingest.py
import os
from datasets import load_dataset
from PIL import Image
import pytesseract
from backend.models.embeddings import embed_texts
import faiss
import numpy as np
import json
from backend.config import settings
from tqdm import tqdm

def ocr_image_bytes(image):
    # `image` may be a path or bytes; dataset returns path-like or PIL.Image in HF
    if isinstance(image, str):
        img = Image.open(image).convert("RGB")
    else:
        img = Image.open(image)
    text = pytesseract.image_to_string(img)
    return text

def build_faiss_from_dataset(save_dir=settings.faiss_index_dir, split="train"):
    ds = load_dataset("Reja1/jee-neet-benchmark", split=split)
    texts = []
    metadatas = []
    for item in tqdm(ds):
        # HF dataset gives "image" (path or Image)
        try:
            txt = ocr_image_bytes(item["image"])
        except Exception as e:
            txt = ""
        # keep metadata fields present in dataset
        metadata = {
            "exam": item.get("exam"),
            "year": item.get("year"),
            "subject": item.get("subject"),
            "type": item.get("type"),
            "answer": item.get("answer"),
            "id": item.get("id", None),
        }
        texts.append(txt)
        metadatas.append(metadata)

    # embed
    embeddings = embed_texts(texts)  # numpy array (N, d)
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(np.array(embeddings).astype("float32"))
    os.makedirs(save_dir, exist_ok=True)
    faiss.write_index(index, os.path.join(save_dir, "jee_neet.index"))

    # save metadata mapping
    with open(os.path.join(save_dir, "jee_neet_meta.jsonl"), "w", encoding="utf-8") as f:
        for meta, text in zip(metadatas, texts):
            meta_record = {"meta": meta, "text": text}
            f.write(json.dumps(meta_record) + "\n")

    print("Saved FAISS index and metadata to", save_dir)
