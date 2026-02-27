from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from app.ingestion.loader import FAQIngestor

router = APIRouter()

class IngestRequest(BaseModel):
    file_path: str = "faq_data.json"

@router.post("/ingest")
def ingest_data(request: IngestRequest):
    try:
        ingestor = FAQIngestor()
        count = ingestor.load_and_index(request.file_path)
        return {"status": "success", "indexed_items": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/ingest/clear")
def clear_database():
    try:
        # Import inside the function to avoid circular imports if any, or just import at top
        from app.db.vector_store import QdrantVectorStore
        store = QdrantVectorStore()
        store.clear_collection()
        return {"status": "success", "message": "Database collection cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
