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
        
        #Handler Properties
        self._handlers = self._build_handler_dict()
        self._active_handlers : list = []
        
        #Result Related Properties
        self._result_dict : dict = {}
        
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
            #Adds document to the library collection
            file_path = self._convert_to_Path(file_path)
            self._current_doc = Document(file_path)
            self._document_collection.append(self._current_doc)
            self._update_doc_total()
            
            #Creates a unique handler for the object
            self._active_handlers.append(self._create_handler(self._current_doc._suffix))
            
        else:
            #Max amount of documents are reached
            self._error_msg(self.add_new_document.__name__, "Document Collection is Full. Please remove a document before attempting to add again.")
    
    def _convert_to_Path(self, str : str) -> str:
        return Path(str)
        
    def _create_handler(self, suffix : str) -> JSONLHandeler:
        if suffix in self._handlers:
            #Create the instance of the handeler
            selected_handeler_class = self._handlers[suffix]
            handeler_instance = selected_handeler_class(self._current_doc)
            
            #Checks the instance before returning it to ensure there is ACTUALLY a instance active
            if isinstance(handeler_instance, JSONLHandeler):
                return handeler_instance
            
        return None
        
    def _get_results_of_handler(self, handler : JSONLHandeler) -> str:
        if handler.check_for_result() <= 0:
            return None
        
        return handler._results.get_details_full()
            
    def search_document_for(self, query : str) -> dict:
        self._clean_results()
        try:
            #Loops through each active handler
            for handler in self._active_handlers:
                if handler:
                    #Let the handler search through the provided files
                    handler.keywords = query
                    handler.search_by_keywords()
                    result_str = self._get_results_of_handler(handler)
                    
                    #Appends to library results
                    self._result_dict[handler.generate_file_dict_key()] = result_str
                else:
                    continue
                
        except Exception as e:
            self._error_msg(self.search_document_for.__name__, e)
            
    def _error_msg(function_name : str, error : str):
        print(f"{function_name} encountered an error: {error}.")
        
    def retrieve_results(self) -> dict:
        return self._result_dict if self._result_dict else None
    
    def _clean_results(self):
        self._result_dict = {}
        
    def view_file_format(self) -> dict:
        files_format = {}
        count = 0
        for handler in self._active_handlers:
            files_format[count] = handler.get_schema()
            
        return files_format
            
    def peek_at_file_content(self) -> list:
        files_format = {}
        count = 0
        for handler in self._active_handlers:
            files_format[count] = handler.get_sample()
            
        return files_format