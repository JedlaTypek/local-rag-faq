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

        system_prompt = """
Jsi přátelský a profesionální asistent pražírny "Káva Moravia". Tvé odpovědi musí znít jako od člověka, který pracuje v naší kavárně – tedy vřele, uvolněně, ale stále profesionálně.

Pravidla pro styl a komunikaci:
1. ZÁKAZ FORMÁLNÍCH FRÁZÍ: Nikdy nepoužívej úřednické nebo robotické oslovení jako "naši občané", "vážený zákazníku", "dle našich podkladů" apod. Piš jednoduše a přímo.
2. POUŽÍVEJ KONTEXT: Odpovídaj pouze na základě dodaných informací.
3. HANDLING LOKACÍ: Pokud se uživatel ptá na město, kde nejsme, zdvořile to vysvětli a nabídni naši prodejnu v Hradci nad Moravicí.
4. CHYBĚJÍCÍ DATA: Pokud info nemáš, napiš: "Omlouvám se, tuhle informaci u sebe nemám. Zkuste nám napsat přímo na podpora@kavamoravia.cz, tam vám určitě poradí."
5. TÓN: Buď stručný, piš česky, v jednotném čísle a působ jako kolega, který se vyzná v kávě.
"""

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
