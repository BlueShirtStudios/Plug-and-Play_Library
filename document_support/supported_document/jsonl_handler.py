import json
from pathlib import Path

from document_support.document import Document
from document_support.ibase_document_handler import iBaseDocumentHandler
from document_support.document_result import DocumentResult

class JSONLHandeler(iBaseDocumentHandler):
    def __init__(self, doc : Document):
        super().__init__(document=doc)
        self._data = None
        self._schema = {}
        self._jsonl_keys = set()
        self._results = DocumentResult
        self._filter_keys : list = []
        
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
          
    def _error_msg(self, function_name : str, error : str):
        print(f"{function_name} encountered an error: {error}.")
        
    def _read_all_keys(self, data : dict, parent_key : str = ""):
        sub_dict : dict = {}
        if isinstance(data, dict):
            try:
                for cur_key, cur_key_data in data.items():
                    #Constructs the key
                    full_key = f"{parent_key}.{cur_key}" if parent_key else cur_key
                    
                    #Adds the key to the the key list
                    self._jsonl_keys.add(full_key)
                    
                    #Builds schema as we work through the lines
                    #If it has a parent key
                    if parent_key:
                        
                        #First Check if sub dict has keys
                        sub_dict = self._schema[parent_key]
                        if self._is_sub_dict_populated(sub_dict) is True:
                            
                            #Checks if key was previously addedd
                            if self._is_key_already_addedd(sub_dict, cur_key) is False: 
                                    sub_dict[cur_key] = {}
                                    self._schema[parent_key] = sub_dict
                        else:
                            sub_dict[cur_key] = {}
                            self._schema[parent_key] = sub_dict
                        
                    #If not have a parent key
                    else:
                        if self._is_key_already_addedd(self._schema, cur_key) is False:
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
                
    def _is_key_already_addedd(self, dictionary : dict, check_key : str) -> bool:
        for key in dictionary.keys():
            if key == check_key:
                return True
            
        return False      
    
    def _is_sub_dict_populated(self, prov_dict : dict) -> bool:
        if len(prov_dict) >= 1:
            return True
        else: False
            
    def search_by_keywords(self):
        #Initalize counter variables
        threshold = 1
        line_num = 0
        
        #Open the file for search
        try:
            with open (self.file._file_path, "r", encoding="utf-8") as f:
                for line in f:
                    #Initailize Variables
                    keys_with_results = 0
                    line_num += 1
                    
                    line_data = json.loads(line)
                    keys_with_results = self.search_across_all_keys(line_data)
                                        
                    #Results are determined if keywords are found in x amount of keys
                    if keys_with_results >= threshold:
                        #Create  instance if needed
                        if isinstance(self._results, DocumentResult) is False:
                            self._results = DocumentResult(
                            name=self.file._full_file_name,
                            path=self.file._file_path
                            )
                            
                        #Otherwise add to the list content
                        self._results.add_to_results(line_data)
                        self._results.update_last_retrieval_time()
                        
        except Exception as e:
            self._error_msg(self.search_by_keywords.__name__, e)
                    
    def search_across_all_keys(self, data : dict = {}, keys_with_results : int = 0) -> int:
        if isinstance(data, dict):      
            #Each key will be checked for a match
            for main_key in data.keys():
                
                #Checks if keys should be looked at
                if main_key in self._filter_keys:
                    continue
                    
                key_value = data[main_key]
                #Skips empty entries
                if key_value is None:
                    continue
                        
                #If found to be a string
                if isinstance(key_value, str):
                    for item in key_value.split():
                        if item in self.keywords:
                            keys_with_results += 1
                            
                #If it is a number - First checks if a number is in the keywords
                for value in self.keywords:
                    if isinstance(value, int| float):
                        #On success
                        if (key_value >= value - 100) or (key_value <= value + 100):
                            keys_with_results += 1
                        
                #Search if found to be a list
                if isinstance(key_value, list):
                    for item in key_value:
                        if isinstance(item, dict):
                            self.search_across_all_keys(item, keys_with_results)
                        
                        elif isinstance(item, str| int |float |bool):
                            if item in self.keywords:
                                keys_with_results += 1   
                            
            return keys_with_results
        
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
            
    def query_filter(self, criteria : str):
        if criteria not in self._jsonl_keys:
            return None
        
        self._filter_keys.append(criteria)
        
    def reset_filter(self):
        self._filter_keys = []
    
    def format_for_agent(self):
        pass
    
    def retrieve_result(self) -> DocumentResult:
        if isinstance(self._results, DocumentResult):
            return self._results
        else:
            return None
    
    def generate_file_dict_key(self) -> str:
        return f"DOC_{self._results._document_name}"
    
    def get_file(self) -> Document:
        return self.file
    