from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class Request(BaseModel):
    data: str

class Response(BaseModel):
    response: str
