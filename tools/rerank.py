from typing import List, Dict
from sentence_transformers import CrossEncoder

class reranker:

    def __init__(self, model_name: str = 'cross-encoder/ms-marco-MiniLM-L-6-v2'):
        self.model = CrossEncoder(model_name)
    
    def rerank(self, query: str, results: List[Dict], top_k: int = 3) -> List[Dict]:
        if not results:
            return []
        
        pairs = [(query, result["content"]) for result in results]

        scores = self.model.predict(pairs)

        scored_results = list(zip(results, scores))
        scored_results.sort(key=lambda x: x[1], reverse=True)

        reranked = []
        for result, score in scored_results[:top_k]:
            result["rerank_score"] = float(score)
            reranked.append(result)
        
        return reranked