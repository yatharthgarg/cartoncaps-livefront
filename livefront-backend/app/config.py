from typing import ClassVar
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./cartonCapsData.sqlite"
    EMBED_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MODEL: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    K_NEIGHBORS: int = 3
    DEFAULT_RECOMMEND_K: int = 2
    MORE_K: int = 2
    RAG_TOP_K: int = 5
    MAX_HISTORY: int = 4
    MAX_NEW_TOKENS: int = 200
    GENERATION_TEMPERATURE: float = 0.7
    GENERATION_TOP_P: float = 0.9
    DEFAULT_REFERRAL_PERCENT: int = 20
    INTENT_THRESHOLD: float = 0.4
    MAX_INPUT_TOKENS: ClassVar[int] = 1024

    class Config:
        env_file = None


settings = Settings()