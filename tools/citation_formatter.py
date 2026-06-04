from typing import List, Dict

def format_single_citation(doc: Dict, index: int) -> str:
    source = doc.get("source", "未知来源")
    url = doc.get("url", "N/A")
    snippet = doc.get("content", "")[:200]

    return f"[{index}] {source}. URL: {url}\n相关段落: {snippet}..."

def format_citations(retrieved_docs: List[Dict]) -> str:
    if not retrieved_docs:
        return ""
    header = "\n\n引用来源:\n"
    citations = []
    for i, doc in enumerate(retrieved_docs, 1):
        citations.append(format_single_citation(doc, i))
    return header + "\n".join(citations)

def answer_with_citations(answer: str, retrieved_docs: List[Dict]) -> str:
    if not retrieved_docs:
        return answer
    citations = format_citations(retrieved_docs)
    return f"{answer}{citations}"