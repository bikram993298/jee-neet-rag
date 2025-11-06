from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import chat as chat_router
from backend.config import HOST, PORT

app = FastAPI(title="jee-neet-rag (RAG only)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.api.main:app", host=HOST, port=PORT, reload=True)
