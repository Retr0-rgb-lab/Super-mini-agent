import re
from typing import List

def chunk_by_sentences(text: str, max_chunk_size: int = 500) -> List[str]:
    sentences = re.split(r'([。！？\n])', text)
    
    merged = []
    for i in range(0, len(sentences) - 1, 2):
        if sentences[i]:
            merged.append(sentences[i] + (sentences[i+1] if i+1 < len(sentences) else ""))
    
    chunks = []
    current_chunk = ""
    
    for sentence in merged:
        if len(current_chunk) + len(sentence) < max_chunk_size:
            current_chunk += sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def chunk_financial_report(content: str, report_name: str, max_chunk_size: int = 500) -> List[dict]:
    chunks = chunk_by_sentences(content, max_chunk_size)
    
    result = []
    for i, chunk in enumerate(chunks):
        result.append({
            "content": chunk,
            "metadata": {
                "report": report_name,
                "chunk_id": i,
                "char_count": len(chunk)
            }
        })
    
    return result