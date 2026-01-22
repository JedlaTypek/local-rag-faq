from fastapi import FastAPI
from app.api_ingest import router as ingest_router
from app.api_ask import router as ask_router

app = FastAPI(title="Easy Local RAG API")

app.include_router(ingest_router, prefix="/api/v1")
app.include_router(ask_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    # Initialize DB connection on startup to verify 
    try:
        store = QdrantVectorStore()
        print(f"Connected to Qdrant at {settings.QDRANT_HOST}:{settings.QDRANT_PORT}")
    except Exception as e:
        print(f"Failed to connect to Qdrant: {e}")

@app.get("/")
def read_root():
    return {"message": "Welcome to Easy Local RAG API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
