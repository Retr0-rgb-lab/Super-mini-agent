import chromadb
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
from typing import List, Dict, Optional
import numpy as np

class HybridRetriver:
    def __init__(self, collection_name: str = "English_texts", alpha: float = 0.5):
        self.client = chromadb.PersistentClient(path = "E:/Finance_AI/agent_project/practice/RAG/data/chroma_db")
        self.collection = self.client.get_or_create_collection(collection_name)
        self.alpha = alpha
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        self.documents: List[str] = []
        self.bm25: Optional[BM25Okapi] = None
        self._bm25_indexed = False
    
    def _ensure_bm25_index(self):
        if not self._bm25_indexed:
            results = self.collection.get()
            self.documents = results["documents"]
            
            if self.documents:
                tokenized_docs = [doc.split() for doc in self.documents]
                self.bm25 = BM25Okapi(tokenized_docs)
                self._bm25_indexed = True
    
    def get_collection(self):
        return self.collection
    
    def embed_text(self, text: str):
        return self.model.encode(text).tolist()
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:       
        embed_query = self.model.encode([query]).tolist()
        vec_results = self.collection.query(
            query_embeddings=embed_query,
            n_results=top_k * 2
        )
        self._ensure_bm25_index()
        bm25_scores = {}
        query_tokens = query.split()
        raw_scores = self.bm25.get_scores(query_tokens)

        for i, doc_id in enumerate(vec_results["ids"][0]):
            if vec_results["documents"][0][i] in self.documents:
                doc_idx = self.documents.index(vec_results["documents"][0][i])
            else:
                doc_idx = -1
            if doc_idx >= 0:
                bm25_scores[doc_id] = raw_scores[doc_idx]

        final_scores = {}
        bm25_max = max(bm25_scores.values()) if bm25_scores else 1
        bm25_norm_factor = bm25_max if bm25_max > 0 else 1
        for i, doc_id in enumerate(vec_results["ids"][0]):
            vec_score = 1 - vec_results["distances"][0][i] / 2
            bm25_score = bm25_scores.get(doc_id, 0)
            bm25_norm = bm25_score / bm25_norm_factor
            
            hybrid_score = self.alpha * bm25_norm + (1 - self.alpha) * vec_score
            final_scores[doc_id] = hybrid_score
        
        sorted_results = sorted(
            final_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]
        
        results = []
        for doc_id, score in sorted_results:
            idx = vec_results['ids'][0].index(doc_id)
            results.append({
                "id": doc_id,
                "content": vec_results['documents'][0][idx],
                "metadata": vec_results['metadatas'][0][idx],
                "hybrid_score": score
            })
        
        return results