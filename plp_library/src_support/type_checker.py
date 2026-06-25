from pathlib import Path

class InputHandler():
    def __init__(self):
        self._input : str | Path = None
        self._expected_type : str | Path = None
        self._type_error_str : str = None
   
    def set_input_values(self, input, expect):
        self._input = input
        self._expected_type = expect
        
    def check_input(self) -> bool:
        if isinstance(self._input, self._expected_type):
            return True
        
        else:
            self._type_error_str = f"Wrongfull Input Provided, Passed Type: {type(self._input)}, Expected: {type(self._expected_type)}"
            return False
            
    def send_error(self):
        return self._type_error_str