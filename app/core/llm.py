from openai import OpenAI
from app.core.config import settings
import ollama # Keep ollama library for direct embedding if needed, or use OpenAI client for everything

class LLMService:
    def __init__(self):
        self.client = OpenAI(
            base_url=settings.OLLAMA_BASE_URL,
            api_key=settings.OLLAMA_API_KEY
        )
        self.model = settings.OLLAMA_MODEL

    def get_embedding(self, text: str):
        # Specific to Ollama embedding endpoint or use ollama python lib directly for efficiency
        # Using ollama lib directly for embeddings as it's often more reliable for local models
        response = ollama.embeddings(model='mxbai-embed-large', prompt=text)
        return response["embedding"]

    def generate_response(self, messages):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1
        )
        return response.choices[0].message.content
