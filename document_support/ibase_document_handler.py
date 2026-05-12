from abc import ABC, abstractmethod
from pathlib import Path
from document_support.document import Document

class iBaseDocumentHandler(ABC):
    def __init__(self, document : Document):
        self._file = document
        self._keywords  = set()
    
    @abstractmethod
    def search_by_keywords(self):
        pass
    
    @abstractmethod
    def get_schema(self):
        pass
    
    @abstractmethod
    def query_filter(self, criteria : str):
        pass
    
    @abstractmethod
    def get_sample(self, n : int):
        pass
    
    @abstractmethod
    def format_for_agent(self):
        pass
    
    @property
    def file(self) -> Document:
        return self._file
    
    @file.setter
    def file(self, file : Document):
        self._file = file
        
    @property
    def keywords(self) -> set:
        return self._keywords
    
    @keywords.setter
    def keywords(self, query : str):
        for word in query.split():
            if len(word) > 3:
                self._keywords.add(word)
                
            else: continue