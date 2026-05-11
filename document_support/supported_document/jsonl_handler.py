import json

from document_support.document import Document
from document_support.ibase_document_handler import iBaseDocumentHandler

class JSONLHandeler(iBaseDocumentHandler):
    def __init__(self, doc : Document):
        super().__init__(document=doc)
        self._data = None
        self._schema = {}
        self._jsonl_keys = set()
        
        #Intialization methods
        self._read_jsonl_file()
        
    def _read_jsonl_file(self, n = 10):
        count = 0
        #Reads the first 10 lines to confirm the keys
        try:
            with open(self._file._file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if count > n:
                        exit
                        
                    try:
                        data = json.loads(line)
                        self._read_all_keys(data)
                        count += 1
                        
                    except Exception as e:
                        self._error_msg(self._read_jsonl_file.__name__, e)
                        continue
                    
        except Exception as e:
            self._error_msg(self._read_jsonl_keys.__name__, e)
          
    def _error_msg(self, function_name : str, error : str):
        print(f"{function_name} encountered an error: {error}.")
        
    def _read_all_keys(self, data, parent_key : str = ""):
        for k, v in data.items():
            try:
                full_key = f"{parent_key}.{k}" if parent_key else k
                    
                self._jsonl_keys.add(full_key)
                                    
                if isinstance(v, dict):
                    self._jsonl_keys.update(self._read_all_keys(v, full_key))
                    
            except Exception as e:
                self._error_msg(self._read_all_keys.__name, e)
                      
            
    def search_by_keywords(self):
        print("Searching............")
        
    def get_sample(self):
        print("Presenting Sample")
        
    def get_schema(self):
        print("Getting Schema")
        
    def query_filter(self, criteria):
        pass
    
    def format_for_agent(self):
        pass