# backend/api/main.py
from fastapi import FastAPI
from backend.api.routes_chat import router as chat_router
from backend.api.routes_admin import router as admin_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Hybrid JEE/NEET Tutor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")
app.include_router(admin_router, prefix="/api/admin")

@app.get("/")
def root():
    return {"status": "ok", "message": "Hybrid JEE/NEET Tutor API"}
