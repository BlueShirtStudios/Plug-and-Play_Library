import json

from document_support.ibase_document_handler import iBaseDocumentHandler

class JSONLHandeler(iBaseDocumentHandler):
    def __init__(self):
        super().__init__()
        self._data = None
        self._schema = {}
        self._jsonl_keys = set()
        
    def _read_jsonl_keys(self, n = 10):
        #Reads the first 10 lines to confirm the keys
        try:
            with open(self._file._file_path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        self._jsonl_keys.update(data.keys())
                        
                    except Exception as e:
                        self._error_msg(self._read_jsonl_keys.__name__, e)
                        continue
                    
        except Exception as e:
            self._error_msg(self._read_jsonl_keys.__name__, e)
          
    def _error_msg(function_name : str, error : str):
        print(f"{function_name} encountered an error: {error}.")
        
    def _check_for_nested_keys(self, keys : set):
        for key in keys:
            if str(key).find('.') is not 0:
                #Get the nested keys
                pass            
            
    def search_by_keywords(self, keywords):
        print("Searching............")