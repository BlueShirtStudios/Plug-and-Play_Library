from pathlib import Path

from document_support.document import Document
from document_support.supported_document.jsonl_handler import JSONLHandeler

class Document_Library():
    def __init__(self):
        #Document Collection Properties
        self._document_collection : list[Document] = []
        self._doc_collection_max = 10
        self._doc_total = 0
        self._doc_limit = 0
        self._current_doc = None
        
        #Active Handeler Properties - revisit this
        
        #Handler Properties
        self._handlers = self._build_handler_dict()
        self._chosen_handler = None
        
    def _build_handler_dict(self) -> dict:
        #Dictionary stores all available handlers
        handlers ={
            ".jsonl" : JSONLHandeler
        }
        return handlers
    
    def _update_doc_total(self):
        self._doc_total += 1
        
    def add_new_document(self, file_path : str):
        #Checks if another one can be added
        if self._doc_total < self._doc_collection_max:
            file_path = self._convert_to_Path(file_path)
            self._current_doc = Document(file_path)
            self._document_collection.append(self._current_doc)
            
        else:
            self._error_msg(self.add_new_document.__name__, "Document Collection is Full. Please remove a document before attempting to add again.")
    
    def _convert_to_Path(self, str : str) -> str:
        return Path(str)
        
    def _call_handler(self):
        if self._current_doc._suffix in self._handlers.keys():
            self._chosen_handler = self._handlers[self._current_doc._suffix](self._current_doc)
            
    def search_by_keyword(self, query : str) -> dict:
        doc_num = 0
        while doc_num <= self._doc_limit:
            self._current_doc = self._document_collection[doc_num]
            self._call_handler()
            self._chosen_handler.keywords = query
            self._chosen_handler.search_by_keywords()
            doc_num += 1
            
    def _error_msg(function_name : str, error : str):
        print(f"{function_name} encountered an error: {error}.")