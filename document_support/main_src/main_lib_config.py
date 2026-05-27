class Library_Configs():
    def __init__(self):
        self._result_format_string = False
        self._result_format_dict = False   
    
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