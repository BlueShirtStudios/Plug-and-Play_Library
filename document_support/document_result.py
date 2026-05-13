from datetime import datetime
from pathlib import Path
import json

class DocumentResult():
    def __init__(self, name : str, path : Path, content : json, page : int):
        self._document_name = name
        self._document_path = path
        self._content = content
        self._found_at = datetime.now()
        self._page = page