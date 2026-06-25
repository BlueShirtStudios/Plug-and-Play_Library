from datetime import datetime
from pathlib import Path

class DocumentResult():
    def __init__(self, name : str, path : Path):
        self._document_name = name
        self._document_path = path
        self._relevant_content : dict = {}
        self._last_retrieval_at = None
        
    def add_to_results(self, line : dict):
        new_index = len(self._relevant_content)
        self._relevant_content[new_index] = line    
        
    def update_last_retrieval_time(self):
        self._last_retrieval_at = datetime.now()
        
    def get_result_str(self) -> str:
        return f"In {self._document_name} the results for the query are: {self._relevant_content}. The last retrieval was made at {self._last_retrieval_at}"
    
    def get_result_dict(self) -> dict:
        return self._relevant_content
    
   