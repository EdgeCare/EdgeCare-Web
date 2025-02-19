from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict

class Request(BaseModel):
    text: str

class Response(BaseModel):
    response: str
    results: List[Dict[str, str]] 
