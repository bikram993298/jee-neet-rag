# backend/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    hf_token: str
    ollama_host: str = "localhost"
    ollama_port: int = 11434
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    faiss_index_dir: str = "./backend/data/faiss_index"
    device: str = "cpu"  # change to 'cuda' if available

    class Config:
        env_file = ".env"

settings = Settings()
