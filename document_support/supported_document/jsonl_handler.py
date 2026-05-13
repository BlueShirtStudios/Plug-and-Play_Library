import json

from document_support.document import Document
from document_support.ibase_document_handler import iBaseDocumentHandler
from document_support.document_result import DocumentResult

class JSONLHandeler(iBaseDocumentHandler):
    def __init__(self, doc : Document):
        super().__init__(document=doc)
        self._data = None
        self._schema = {}
        self._jsonl_keys = set()
        self._result_doc_list : list[DocumentResult] = []
        
        #Intialization method
        self._read_jsonl_file_for_keys()
        
    def _read_jsonl_file_for_keys(self, n = 10):
        count = 0
        #Reads the first 10 lines to confirm the keys
        try:
            with open(self._file._file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if count > n:
                        break
                        
                    try:
                        data = json.loads(line)
                        self._read_all_keys(data)
                        count += 1
                        
                    except Exception as e:
                        self._error_msg(self._read_jsonl_file_for_keys.__name__, e)
                        continue
        
        except json.JSONDecodeError as e:
            self._error_msg(self._read_jsonl_file_for_keys.__name__, e)            
        
        except Exception as e:
            self._error_msg(self._read_jsonl_file_for_keys.__name__, e)
            
        print(self._jsonl_keys)
          
    def _error_msg(self, function_name : str, error : str):
        print(f"{function_name} encountered an error: {error}.")
        
    def _read_all_keys(self, data, parent_key : str = ""):
        sub_dict : dict = {}
        if isinstance(data, dict):
            try:
                for cur_key, cur_key_data in data.items():
                    #Constructs the key
                    full_key = f"{parent_key}.{cur_key}" if parent_key else cur_key
                    
                    #Adds the key to the the key list
                    self._jsonl_keys.add(full_key)
                    
                    #Builds schema as we work through the lines
                    if parent_key:
                        sub_dict[cur_key] = {}
                        self._schema[parent_key] = sub_dict
                    else:
                        self._schema[cur_key] = {}    
                    
                    #Searches through content to determine if there are nested keys
                    if isinstance(cur_key_data, list):
                        for item in cur_key_data:
                            if isinstance(cur_key_data, dict):
                                self._read_all_keys(item, full_key)
                                
                            elif isinstance(item, dict):
                                self._read_all_keys(item, cur_key)
                    
            except Exception as e:
                self._error_msg(self._read_all_keys.__name__, e)           
            
    def search_by_keywords(self):
        #Initalize counter variables
        total_keys = len(self._jsonl_keys)
        threshold = total_keys * 0.5
        line_num = 0
        
        #Open the file for search
        with open (self.file._file_path, "r", encoding="utf-8") as f:
            for line in f:
                keys_with_results = 0
                line_num += 1
                try:
                    line_data = json.loads(line)
                    
                    #Each key will be checked for a match
                    for key in self._jsonl_keys:
                        value = line_data[key].get(key, None)
                        if value is None:
                            continue
                        
                        if value in self.keywords:
                            keys_with_results += 1
                            
                    #Results are determined if keywords are found in x amount of keys
                    if keys_with_results > threshold:
                        result_doc = DocumentResult(
                            name=self.file._full_file_name,
                            path=self.file._file_path,
                            content=line,
                            page=line_num
                        )
                        
                        self._result_doc_list.append(result_doc)
                        
                except json.JSONDecodeError:
                    continue
                
                except Exception as e:
                    self._error_msg(self.search_by_keywords.__name__, e)
        
    def get_sample(self, allowed_peek_lines : int = 10) -> list:
        sample = []
        lines_read = 0
        
        with open(self.file._file_path, "r", encoding="utf=8") as f:
            for line in f:
                if lines_read >= allowed_peek_lines:
                    break
                
                try:
                    jsonl_line = json.loads(line)
                    sample.append(jsonl_line)
                    lines_read += 1 
                    
                except json.JSONDecodeError:
                    continue
                
                except Exception as e:
                    self._error_msg(self.get_sample.__name__, e)
                    
        return sample         
     
    def get_schema(self) -> dict:
        return self._schema
            
    def query_filter(self, criteria):
        pass
    
    def format_for_agent(self):
        pass