import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")

    MISTRAL_CHAT_MODEL: str = os.getenv("MISTRAL_CHAT_MODEL", "mistral-small-latest")


    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")


    WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "small")

    
    DATA_DIR: str = os.getenv("DATA_DIR", os.path.join(os.path.dirname(__file__), "data"))
    AUDIO_DIR: str = os.path.join(DATA_DIR, "audio")
    CHROMA_DIR: str = os.path.join(DATA_DIR, "chroma")

    
    AUDIO_CHUNK_MINUTES: int = int(os.getenv("AUDIO_CHUNK_MINUTES", "5"))
    RAG_CHUNK_SIZE: int = int(os.getenv("RAG_CHUNK_SIZE", "1000"))
    RAG_CHUNK_OVERLAP: int = int(os.getenv("RAG_CHUNK_OVERLAP", "150"))

    
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")


settings = Settings()

os.makedirs(settings.AUDIO_DIR, exist_ok=True)
os.makedirs(settings.CHROMA_DIR, exist_ok=True)
