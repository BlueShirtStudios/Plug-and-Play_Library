class Library_Configs():
    def __init__(self):
        self._result_format_string = False
        self._result_format_dict = False   
        self._supported_documents : list = []
    
    @property
    def result_format_string(self) -> bool:
        return self._result_format_string
    
    @result_format_string.setter
    def result_format_string(self, value : bool):
        self._result_format_string = value
        
    @property
    def result_format_dict(self) -> bool:
        return self._result_format_dict
    
    @result_format_dict.setter
    def result_format_dict(self, value : bool):
        self._result_format_dict = value
        
    @property
    def supported_documents(self) -> list:
        return self._supported_documents
    
    @supported_documents.setter
    def supported_documents(self, value : list):
        self._supported_documents = value
        
    def _initialize_support_documents(self):
        self.supported_documents = [".jsonl"]
        
