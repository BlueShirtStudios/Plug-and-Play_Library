from pathlib import Path
from datetime import datetime

class Document():
    def __init__(self, file_path : Path):
        #Check of the file exists
        if self._ensure_file_exists(file_path) is False:
            return None
        
        self._file_path = file_path
        
        #File Properties
        self._full_file_name = self._file_path.name
        self._suffix = self._file_path.suffix
        self._size = self._file_path.stat().st_size
        self._parent = self._file_path.parent
        self._anchor = self._file_path.anchor
        
        #Other extras
        self._time_addedd = datetime.now()
        self._index = None
        
    def _ensure_file_exists(self, file_path) -> bool:
        if file_path.exists() is False:
            return False
        
        else: return True