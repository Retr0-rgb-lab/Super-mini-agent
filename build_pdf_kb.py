import sys
import glob
import os

sys.path.insert(0, 'E:/Finance_AI/agent_project/practice/supermini_agent')

from tools.pdf_loader import PDFLoader
from tools.emb_pipe import DocumentEmbedder

def import_pdf_to_kb(
    pdf_path: str, 
    collection_name: str = "financial_kb", 
    metadata: dict = None,
    clear_existing: bool = False
) -> dict:
    loader = PDFLoader()
    chunks = loader.load_and_chunk(pdf_path, metadata=metadata)
    
    embedder = DocumentEmbedder()
    
    if clear_existing:
        embedder.delete_collection(collection_name)
    
    count = embedder.embed_documents(chunks, collection_name)
    
    return {
        "file": os.path.basename(pdf_path),
        "chunks": count,
        "collection": collection_name
    }


def import_multiple_pdfs(
    pdf_glob_pattern: str,
    collection_name: str = "financial_kb",
    clear_existing: bool = False
) -> list:
    pdf_files = glob.glob(pdf_glob_pattern)
    if not pdf_files:
        print(f"No PDF files found matching: {pdf_glob_pattern}")
        return []
    
    loader = PDFLoader()
    embedder = DocumentEmbedder()
    
    if clear_existing:
        embedder.delete_collection(collection_name)
    
    results = []
    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path}")
        chunks = loader.load_and_chunk(pdf_path)
        count = embedder.embed_documents(chunks, collection_name)
        results.append({
            "file": os.path.basename(pdf_path),
            "chunks": count
        })
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Import PDF files to ChromaDB knowledge base")
    parser.add_argument("pdf_path", help="Path to PDF file or glob pattern (e.g., data/*.pdf)")
    parser.add_argument("--collection", "-c", default="financial_kb", help="Collection name (default: financial_kb)")
    parser.add_argument("--clear", action="store_true", help="Clear existing collection before import")
    parser.add_argument("--company", help="Company name to add as metadata")
    parser.add_argument("--year", type=int, help="Year to add as metadata")
    
    args = parser.parse_args()
    
    metadata = {}
    if args.company:
        metadata["company"] = args.company
    if args.year:
        metadata["year"] = args.year
    
    if "*" in args.pdf_path:
        results = import_multiple_pdfs(
            args.pdf_path,
            collection_name=args.collection,
            clear_existing=args.clear
        )
        print(f"\nImported {len(results)} files:")
        for r in results:
            print(f"  - {r['file']}: {r['chunks']} chunks")
    else:
        result = import_pdf_to_kb(
            args.pdf_path,
            collection_name=args.collection,
            metadata=metadata if metadata else None,
            clear_existing=args.clear
        )
        print(f"\nImported: {result['file']}")
        print(f"  Chunks: {result['chunks']}")
        print(f"  Collection: {result['collection']}")