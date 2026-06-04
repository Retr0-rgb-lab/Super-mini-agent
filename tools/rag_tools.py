from .retrieval_pipeline import RetrievalPipeline
from typing import Union, List, Dict

_pipeline: Union[RetrievalPipeline, None] = None

def init_rag_tools(collection_name: str = "financial_kb"):
    global _pipeline
    _pipeline = RetrievalPipeline(collection_name)

def lookup_financial_report(query: str, top_k: int = 3) -> str:
    if _pipeline is None:
        return "RAG 知识库未初始化，请先调用 init_rag_tools()"
    
    results = _pipeline.retrieve(query)
    if not results:
        return []
    
    context_parts = []
    for i, result in enumerate(results, 1):
        score = result.get('rerank_score', result.get('hybrid_score', 0))
        context_parts.append(
            f"【文档{i}】（相似度: {score:.2%}）\n{result['content']}"
        )
    
    header = "根据知识库检索结果：\n"
    footer = "\n\n请基于以上信息回答用户问题。如果信息不足，可以结合通用知识补充。"
    
    return header + "\n\n".join(context_parts) + footer

def retrieve_structured(query: str, top_k: int = 3) -> List[Dict]:
    if _pipeline is None:
        return []
    return _pipeline.retrieve(query)