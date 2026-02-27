from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    COLLECTION_NAME: str = "faq_collection"
    
    # LLM Settings
    OLLAMA_BASE_URL: str = "http://localhost:11434/v1"
    OLLAMA_MODEL: str = "llama3"
    OLLAMA_EMBEDDING_MODEL: str = "mxbai-embed-large"
    OLLAMA_API_KEY: str = "ollama" # Dummy key for local

    class Config:
        env_file = ".env"

settings = Settings()
