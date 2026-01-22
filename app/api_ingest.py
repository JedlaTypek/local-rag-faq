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
