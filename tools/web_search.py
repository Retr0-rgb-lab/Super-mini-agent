from tavily import TavilyClient
from typing import Dict, List, Optional
import os

class WebSearcher:
    def __init__(self, api_key: Optional[str] = None):
        self.client = TavilyClient(api_key=api_key or os.getenv("TAVILY_API_KEY"))
    
    def search(self, query: str, num_results: int = 5) -> List[Dict]:
        results = self.client.search(query, num_results=num_results)
        return results.get('results', [])
    
    def search_with_context(self, query: str, num_results: int = 5, max_tokens: int = 4000) -> str:
        response = self.client.search(
            query, 
            num_results=num_results,
            max_tokens=max_tokens, 
            include_answer=True,
            include_raw_content=False
        )
        answer = response.get('answer', "")
        if not answer:
            results = response.get('results', [])
            if results:
                answer = "\n".join([f"- {r['title']}: {r['content'][:200]}..." for r in results[:3]])
        return answer
    
    def get_full_content(self, query: str) -> List[Dict]:
        response = self.client.search(query, include_raw_content=True)
        return response.get('results', [])