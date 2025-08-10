# api/__init__.py
"""
API package for serving RAG-based summarization and citation lookup.
"""

from fastapi import FastAPI
from .routes import summarization_router, citation_router

app = FastAPI(
    title="Smart Research Paper Summarizer & Citation Finder",
    description="Upload research papers → get summaries + related citations",
    version="1.0.0"
)

# Include routes
app.include_router(summarization_router, prefix="/summarize", tags=["Summarization"])
app.include_router(citation_router, prefix="/citations", tags=["Citations"])

__all__ = ["app"]
