import asyncio
from app.rag.engine import RAGEngine
from app.evaluation.metrics import MetricsEvaluator
import json

# Sample Ground Truth Data for Eval
EVAL_DATA = [
    {
        "question": "Jaké jsou otevírací hodiny?",
        "ground_truth": "Máme otevřeno každý všední den od 8:00 do 17:00."
    },
    {
        "question": "Kde vás najdu?",
        "ground_truth": "Sídlíme na adrese Vodičkova 123, Praha 1."
    }
]

async def run_evaluation():
    print("Starting Evaluation...")
    engine = RAGEngine()
    evaluator = MetricsEvaluator()
    
    results = []
    
    for item in EVAL_DATA:
        query = item["question"]
        truth = item["ground_truth"]
        
        print(f"Processing: {query}")
        
        # 1. Get Answer from RAG
        rag_response = engine.ask(query)
        generated_answer = rag_response["answer"]
        
        # 2. Evaluate
        metrics = evaluator.evaluate_response(query, generated_answer, truth)
        metrics["generated_answer"] = generated_answer
        metrics["ground_truth"] = truth
        
        results.append(metrics)
        print(f"Results for '{query}': {metrics}")

    # Summary
    print("\n--- Evaluation Summary ---")
    avg_cosine = sum(r["cosine_similarity"] for r in results) / len(results)
    print(f"Average Cosine Similarity: {avg_cosine:.4f}")
    
if __name__ == "__main__":
    asyncio.run(run_evaluation())
