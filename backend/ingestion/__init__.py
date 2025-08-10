# ingestion/__init__.py
"""
Ingestion package for loading PDFs, chunking text, generating embeddings, 
and storing them in Pinecone for retrieval.
"""

from .loader import load_paper
from .chunker import chunk_text
from .embedder import embed_chunks
from .pinecone_client import store_embeddings

__all__ = [
    "load_paper",
    "chunk_text",
    "embed_chunks",
    "store_embeddings",
]
