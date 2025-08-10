# backend/api/routes_admin.py
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from backend.ingestion.jee_neet_ingest import build_faiss_from_dataset
from backend.ingestion.ncert_ingest import ingest_ncert_from_folder
import os

router = APIRouter()

class ReindexRequest(BaseModel):
    dataset: str  # "jee_neet" or "ncert"
    source_path: str = None

@router.post("/reindex")
def reindex(req: ReindexRequest, background: BackgroundTasks):
    if req.dataset == "jee_neet":
        background.add_task(build_faiss_from_dataset)
        return {"status": "started", "dataset": "jee_neet"}
    elif req.dataset == "ncert":
        if not req.source_path:
            return {"status": "error", "message": "source_path required for ncert"}
        background.add_task(ingest_ncert_from_folder, req.source_path)
        return {"status": "started", "dataset": "ncert"}
    else:
        return {"status": "error", "message": "unknown dataset"}
