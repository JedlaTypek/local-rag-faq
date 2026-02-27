import json
import uuid
from typing import List, Dict
from qdrant_client.http import models
from app.core.llm import LLMService
from app.db.vector_store import QdrantVectorStore

class FAQIngestor:
    def __init__(self):
        self.llm_service = LLMService()
        self.vector_store = QdrantVectorStore()

    def load_and_index(self, json_path: str):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        points = []
        for item in data:
            question = item.get("question")
            answer = item.get("answer")
            
            if not question or not answer:
                continue

            # Embed only the question
            vector = self.llm_service.get_embedding(question)
            
            # Create payload
            payload = {
                "question": question,
                "answer": answer,
                "type": "faq"
            }

            # Create deterministic ID based on the question hash
            # This ensures same question gets same ID, overwriting previous versions
            record_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, question))

            # Create Point
            point = models.PointStruct(
                id=record_id,
                vector=vector,
                payload=payload
            )
            points.append(point)

        # Batch upsert
        if points:
            self.vector_store.upsert(points)
            return len(points)
        return 0
