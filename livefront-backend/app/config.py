from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # SQLite DB file URL (aiosqlite)
    DATABASE_URL: str = Field(
        "sqlite+aiosqlite:///./cartonCapsData.sqlite",
        description="SQLite database connection URL"
    )

    # Embedding model for RAG
    EMBED_MODEL: str = Field(
        "sentence-transformers/all-MiniLM-L6-v2",
        description="Sentence-Transformers model for embeddings"
    )

    # Open-source LLM for chat
    LLM_MODEL: str = Field(
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        description="HuggingFace model identifier for text-generation"
    )

    # Legacy retrieval neighbors count (used in RAGService.retrieve)
    K_NEIGHBORS: int = Field(
        10,
        description="Number of neighbors for retrieval (top-k)"
    )

    # How many RAG hits to fetch (alias for K_NEIGHBORS)
    RAG_TOP_K: int = Field(
        10,
        description="Number of top FAISS hits to fetch"
    )

    # Recommendation batch sizes
    DEFAULT_RECOMMEND_K: int = Field(
        2,
        description="Number of products to recommend on first ask"
    )
    MORE_K: int = Field(
        2,
        description="Number of additional recommendations when user asks for more"
    )

    # Conversation context window size
    MAX_HISTORY: int = Field(
        4,
        description="Number of past turns to include in prompt history"
    )

    # Generation parameters
    MAX_NEW_TOKENS: int = Field(
        200,
        description="Maximum tokens to generate in a response"
    )
    GENERATION_TEMPERATURE: float = Field(
        0.7,
        description="Sampling temperature for generation"
    )
    GENERATION_TOP_P: float = Field(
        0.9,
        description="Top-p nucleus sampling probability"
    )

    # Referral program default percentage
    DEFAULT_REFERRAL_PERCENT: int = Field(
        20,
        description="Default percentage of purchase donated via referral"
    )

    # Input token limit for prompt management
    MAX_INPUT_TOKENS: int = Field(
        1024,
        description="Maximum tokens allowed in input prompt"
    )

    # Threshold for future intent classification
    INTENT_THRESHOLD: float = Field(
        0.4,
        description="Threshold for intent matching in user messages"
    )

    class Config:
        env_file = ".env"

settings = Settings()