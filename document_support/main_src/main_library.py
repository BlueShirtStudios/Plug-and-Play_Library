from pathlib import Path

from document_support.main_src.main_lib_config import Library_Configs
from document_support.document_cls.document import Document
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
        
        #Configurations
        self._configs = Library_Configs()
        
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
        
    def _get_results_of_handler(self, handler : JSONLHandeler) -> str | dict:
        #Get the result instance of the handler
        result_obj = handler.retrieve_result()
        if result_obj is None:
            return None
        
        #Determine which format to return
        if self._configs.result_format_string == True:
            return result_obj.get_result_str()
            
        elif self._configs.result_format_dict == True:
            return result_obj.get_result_dict()
        
    def toggle_result_format_toString(self, val : bool):
        self._configs.result_format_string = val
        
    def toggle_result_format_toDict(self, val : bool):
        self._configs.result_format_dict = val
            
    def search_document_for(self, query : str):
        #Clean results of previous search
        self._clean_results()
        try:
            #Loops through each active handler
            for handler in self._active_handlers:
                if handler:
                    #Let the handler search through the provided files
                    handler.keywords = query
                    handler.search_by_keywords()
                    result = self._get_results_of_handler(handler)
                    
                    #Appends to library results
                    if result:
                        self._result_dict[handler.generate_file_dict_key()] = result

                else:
                    continue
                
        except Exception as e:
            self._error_msg(self.search_document_for.__name__, e)
            
    def _error_msg(self,function_name : str, error : str):
        print(f"------- ERROR at {function_name} : {error}. -------")
        
    def retrieve_results(self) -> dict:
        return self._result_dict if self._result_dict else None
    
    def _clean_results(self):
        self._result_dict = {}
        
    def _get_file_suffix(self, file_name : str) -> str:
        dot_pos = file_name.find('.')
        return file_name[dot_pos:] 
    
    def _file_with_handler(self, file_name : str, suffix : str) -> JSONLHandeler:
        #Search which handler is related to the provided file and return the handler
        for handler in self._active_handlers:
            doc = handler.get_file()
            if (doc.get_file_name() == file_name) and (doc.get_file_suffix() == suffix):
                return handler
            
            else: return None
        
    def view_all_file_format(self) -> dict:
        #Returns all active handler's file schema
        files_format = {}
        count = 0
        for handler in self._active_handlers:
            files_format[count] = handler.get_schema()
            count += 1
            
        return files_format
    
    def view_file_format(self, file_name : str) -> dict:
        #Returns a selected file's schema
        suffix = self._get_file_suffix(file_name)
        handler = self._file_with_handler(file_name, suffix)
        if handler:
            return handler.get_schema()
        
        else: return None
            
    def peek_at_all_file_content(self) -> list:
        #Returns all files first few lines
        files_format = {}
        count = 0
        for handler in self._active_handlers:
            files_format[count] = handler.get_sample()
            
        return files_format
    
    def peek_file_content(self, file_name : str) -> dict:
        #Return firsy few lines of provfeded file
        suffix = self._get_file_suffix(file_name)
        handler = self._file_with_handler(file_name, suffix)
        if handler:
            return handler.get_sample()
        
        else: return None
    
    def apply_filter_for_file(self, file_name : str, filter_criteria : str):
        #Get suffix of the file
        suffix = self._get_file_suffix(file_name)
        
        #Check each handler's file for match
        handler = self._file_with_handler(file_name, suffix)
        if handler:
            keys = filter_criteria.split(',')
            for key in keys:
                handler.query_filter(key)   
                    
    def reset_filter_for_file(self, file_name : str):
        suffix = self._get_file_suffix(file_name)
        handler = self._file_with_handler(file_name, suffix)
        if handler:
            handler.reset_filter()
            
    def remove_file_from_library(self, file_name : str):
        try:
            for document in self._document_collection:
                if document._full_file_name == file_name:
                    #Removes the document from the collection
                    index = self._document_collection.index(document)
                    self._document_collection.pop(index)
                    
                    #Free the handler of the document
                    suffix = self._get_file_suffix(file_name)
                    handler = self._file_with_handler(file_name, suffix)
                    if handler:
                        index = self._active_handlers.index(handler)
                        self._active_handlers.pop(index)
                        
        except Exception as e:
            self._error_msg(self.remove_file_from_library.__name__, e)   