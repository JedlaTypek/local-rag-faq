from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from sklearn.metrics.pairwise import cosine_similarity
from app.core.llm import LLMService
import numpy as np

class MetricsEvaluator:
    def __init__(self):
        self.llm_service = LLMService()
        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)

    def calculate_bleu(self, reference: str, candidate: str) -> float:
        # Simple tokenization for BLEU
        ref_tokens = reference.lower().split()
        cand_tokens = candidate.lower().split()
        smoothie = SmoothingFunction().method4
        return sentence_bleu([ref_tokens], cand_tokens, smoothing_function=smoothie)

    def calculate_rouge(self, reference: str, candidate: str) -> dict:
        scores = self.rouge_scorer.score(reference, candidate)
        return {
            "rouge1": scores["rouge1"].fmeasure,
            "rougeL": scores["rougeL"].fmeasure
        }

    def calculate_cosine_similarity(self, text1: str, text2: str) -> float:
        vec1 = self.llm_service.get_embedding(text1)
        vec2 = self.llm_service.get_embedding(text2)
        return cosine_similarity([vec1], [vec2])[0][0]

    def evaluate_response(self, question: str, generated_answer: str, ground_truth: str):
        bleu = self.calculate_bleu(ground_truth, generated_answer)
        rouge = self.calculate_rouge(ground_truth, generated_answer)
        cosine = self.calculate_cosine_similarity(ground_truth, generated_answer)

        return {
            "question": question,
            "bleu_score": bleu,
            "rouge_score": rouge,
            "cosine_similarity": cosine
        }
