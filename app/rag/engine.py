from typing import List, Dict
from app.core.llm import LLMService
from app.db.vector_store import QdrantVectorStore

class RAGEngine:
    def __init__(self):
        self.llm_service = LLMService()
        self.vector_store = QdrantVectorStore()

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        query_vector = self.llm_service.get_embedding(query)
        search_results = self.vector_store.search(query_vector, top_k)
        
        results = []
        for hit in search_results:
            results.append({
                "question": hit.payload.get("question"),
                "answer": hit.payload.get("answer"),
                "score": hit.score
            })
        return results

    def generate(self, query: str, context: List[Dict]) -> str:
        if not context:
            return "Omlouvám se, ale na tuto otázku neznám odpověď z dostupných informací."

        # Prepare context string
        context_str = "\n\n".join([f"Otázka: {item['question']}\nOdpověď: {item['answer']}" for item in context])

        system_prompt = """Jsi užitečný asistent pro zákaznickou podporu. 
Odpovídej na otázky POUZE na základě poskytnutého kontextu. 
Pokud kontext neobsahuje odpověď, řekni, že nevíš.
Odpovídej česky, zdvořile a stručně."""

        user_prompt = f"""Kontext:
{context_str}

Uživatelova otázka: {query}

Odpověď:"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        return self.llm_service.generate_response(messages)

    def ask(self, query: str) -> Dict:
        context = self.retrieve(query)
        answer = self.generate(query, context)
        return {
            "query": query,
            "answer": answer,
            "context": context
        }
