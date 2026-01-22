from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.core.config import settings

class QdrantVectorStore:
    def __init__(self):
        self.client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
        self.collection_name = settings.COLLECTION_NAME
        self._ensure_collection()

    def _ensure_collection(self):
        collections = self.client.get_collections()
        if not any(c.name == self.collection_name for c in collections.collections):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1024,  # Adjust based on embedding model (mxbai-embed-large is 1024)
                    distance=models.Distance.COSINE
                )
            )

    def upsert(self, points):
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(self, vector, top_k=5):
        return self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=top_k
        )
