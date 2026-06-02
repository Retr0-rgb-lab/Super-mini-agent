from langchain_community.document_loaders import PyMuPDFLoader
from typing import List, Optional, Any
import os
import sys

sys.path.insert(0, 'E:/Finance_AI/agent_project/practice/supermini_agent')
from tools.chunker import chunk_financial_report

class PDFLoader:
    def __init__(self, chunk_size: int = 500):
        self.chunk_size = chunk_size
    
    def load(self, file_path: str) -> List[Any]:
        loader = PyMuPDFLoader(file_path)
        return loader.load()
    
    def load_and_chunk(self, file_path: str, metadata: Optional[dict] = None) -> List[dict]:
        documents = self.load(file_path)
        base_name = os.path.basename(file_path)
        chunks = []
        
        for doc in documents:
            if doc.page_content.strip():
                doc_chunks = chunk_financial_report(
                    doc.page_content, 
                    base_name
                )
                for chunk in doc_chunks:
                    chunk_entry = {
                        "content": chunk["content"],
                        "metadata": {
                            **chunk["metadata"],
                            "source_file": base_name,
                            "page_info": doc.metadata.get("page", 0) if hasattr(doc, 'metadata') and doc.metadata else 0
                        }
                    }
                    if metadata:
                        chunk_entry["metadata"].update(metadata)
                    chunks.append(chunk_entry)
        
        return chunks
    
    def load_multiple(self, file_paths: List[str], collection_name: str = None) -> List[dict]:
        all_chunks = []
        for path in file_paths:
            chunks = self.load_and_chunk(path)
            all_chunks.extend(chunks)
        return all_chunks