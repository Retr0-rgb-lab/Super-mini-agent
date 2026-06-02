from .hybrid import HybridRetriver
from .rerank import reranker
from typing import List, Dict, Optional

class RetrievalPipeline:

    def __init__(self, collection_name: str = "financial_kb"):
        self.retriver = HybridRetriver(collection_name, alpha = 0.3)
        self.reranker = reranker()
        self.default_top_k = 10
        self.final_top_k = 3

    def retrieve(self, query: str, use_rerank: bool = True) -> List[Dict]:
        results = self.retriver.search(query, self.default_top_k)
        if not results:
            return []
        
        if use_rerank:
            results = self.reranker.rerank(query, results, self.final_top_k)
        else:
            results = results[:self.final_top_k]
        
        return results