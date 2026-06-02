from sentence_transformers import SentenceTransformer
from pathlib import Path
import chromadb
from typing import List, Dict

class DocumentEmbedder:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.client = chromadb.PersistentClient(path="E:/Finance_AI/agent_project/practice/RAG/data/chroma_db")
        self.collections = {}

    def embed_documents(self, documents: List[Dict], collection_name: str):
        docs = [doc["content"] for doc in documents]
        metas = [doc.get("metadata", {}) for doc in documents]
        ids = [f"doc_{i}" for i in range(len(documents))]

        embed_docs = self.model.encode(docs).tolist()

        collection = self.client.get_or_create_collection(collection_name)
        collection.add(
            documents=docs,
            metadatas=metas,
            ids=ids,
            embeddings=embed_docs
        )

        self.collections[collection_name] = collection

        return len(docs)
    
    def embed_query(self, query: str) -> List[float]:
        return self.model.encode([query])[0].tolist()
    
    def query(self, question: str, collection_name: str):
        emb_query = self.embed_query(question)
        results = self.collections[collection_name].query(
            query_embeddings=emb_query,
            n_results=3
        )
        return results