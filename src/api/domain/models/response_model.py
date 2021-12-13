from typing import List
from pydantic import BaseModel

class ResponseModel(BaseModel):
    data: List[BaseModel]
    code: int
    message: str
