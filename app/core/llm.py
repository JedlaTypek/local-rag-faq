from openai import OpenAI
from app.core.config import settings
from ollama import Client

class LLMService:
    def __init__(self):
        base_url = settings.OLLAMA_BASE_URL
        
        # Ensure OpenAI client has the /v1 suffix
        openai_url = base_url
        if not openai_url.endswith("/v1") and not openai_url.endswith("/v1/"):
            openai_url = openai_url.rstrip("/") + "/v1"
            
        self.client = OpenAI(
            base_url=openai_url,
            api_key=settings.OLLAMA_API_KEY
        )
        
        # Ensure native Ollama client DOES NOT have the /v1 suffix
        ollama_host = base_url.replace("/v1/", "").replace("/v1", "").rstrip("/")
        self.ollama_client = Client(host=ollama_host)
        
        self.model = settings.OLLAMA_MODEL

    def get_embedding(self, text: str):
        # Specific to Ollama embedding endpoint using instantiated client with correct host
        response = self.ollama_client.embeddings(model=settings.OLLAMA_EMBEDDING_MODEL, prompt=text)
        return response["embedding"]

    def generate_response(self, messages):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1
        )
        return response.choices[0].message.content
