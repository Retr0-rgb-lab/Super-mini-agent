# citation_validator.py
import re
from typing import List, Dict, Tuple

class CitationValidator:
    """验证引用有效性和完整性"""
    
    def __init__(self, retrieved_docs: List[Dict]):
        self.retrieved_docs = retrieved_docs
        self.num_docs = len(retrieved_docs)
    
    def extract_citations(self, text: str) -> List[str]:
        """从文本中提取所有引用标记"""
        pattern = r'\[(\d+)\]'
        matches = re.findall(pattern, text)
        return list(set(matches))  # 去重
    
    def validate(self, text: str) -> Dict:
        """
        验证文本中的引用
        
        Returns:
            {
                "valid": bool,
                "issues": [str],
                "missing": [int],
                "out_of_range": [int]
            }
        """
        citations = self.extract_citations(text)
        issues = []
        out_of_range = []
        missing = []
        
        for cite in citations:
            try:
                idx = int(cite)
                if idx < 1 or idx > self.num_docs:
                    issues.append(f"引用 [{cite}] 超出范围（1-{self.num_docs}）")
                    out_of_range.append(idx)
            except ValueError:
                issues.append(f"无效的引用格式：[{cite}]")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "out_of_range": out_of_range,
            "missing": missing
        }
    
    def get_cited_documents(self, text: str) -> List[Dict]:
        """获取被引用的文档"""
        citations = self.extract_citations(text)
        cited = []
        
        for cite in citations:
            try:
                idx = int(cite) - 1  # 转为 0-based index
                if 0 <= idx < self.num_docs:
                    cited.append(self.retrieved_docs[idx])
            except ValueError:
                continue
        
        return cited
    
    def validate_source_attribution(self, text: str) -> Dict:
        """验证来源归属"""
        issues = []
        
        for i, doc in enumerate(self.retrieved_docs, 1):
            source = doc.get("source", "").lower()
            # 检查回答中是否提到了这个来源
            if source and source.lower() not in text.lower():
                issues.append(f"文档 {i} ({source}) 未在回答中被提及")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }